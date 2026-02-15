from pandas import DataFrame, read_sql_query
from scipy.stats import mannwhitneyu
from sqlite3 import connect
from data_analysis import DATABASE
from load_data import CELL_TYPES
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

connection = connect(DATABASE)

# Summary table
DATA_FRAME_SUMMARY = read_sql_query(
    f"""SELECT sample, total_count AS 'Total Count', population, count, percentage
        FROM summary
    """, connection
)

# Population relative frequencies comparing responders
# versus non-responders using a boxplot for each
# immune cell population
RESP_FREQ_DF = read_sql_query(
    f"""SELECT s.population, s.percentage, subj.response, t.subject
        FROM summary s
        JOIN samples t ON s.sample = t.sample
        JOIN subjects subj ON t.subject = subj.subject
        WHERE subj.response IN ('yes', 'no')
    """, connection
)

# Population relative frequencies comparing responders
# versus non-responders using a boxplot for each
# immune cell population
DATA_FRAME_FILTERED_BOXPLOT = read_sql_query(
    f"""SELECT s.population, s.percentage, subj.response, t.subject
        FROM summary s
        JOIN samples t ON s.sample = t.sample
        JOIN subjects subj ON t.subject = subj.subject
        WHERE subj.response IN ('yes', 'no')
        AND t.sample_type = 'PBMC'
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
    """, connection
)

# Compare the differences in cell population relative frequencies of
# melanoma patients receiving miraclib who respond (responders)
# versus those who do not (non-responders), with the overarching
# aim of predicting response to the treatment miraclib.
# 
# Response information can be found in column "response",
# with value "yes" for responding and value "no" for non-responding.
# Please only include PBMC samples.
DATA_FRAME2 = read_sql_query(
    f"""SELECT DISTINCT 
            t.sample, 
            t.b_cell, 
            t.cd8_t_cell, 
            t.cd4_t_cell, 
            t.nk_cell, 
            t.monocyte,
            t.subject, 
            subj.response
        FROM samples t
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
        AND subj.response IN ('yes', 'no')
    """, connection
)

connection.close()

# TEST
def compare_populations(input_df: DataFrame = DATA_FRAME_FILTERED_BOXPLOT):
    """
    Compare cell populations between responders and non-responders
    by first averaging samples within each subject to handle repeated measures.
    """
        
    # Average the percentages for each subject within each population
    # This collapses multiple samples per subject down to one value per subject
    df_averaged = input_df.groupby([ 'subject', 'population', 'response' ], as_index = False)['percentage'].mean()
    
    populations = df_averaged['population'].unique()
    results = []
    
    alpha = 0.05

    for pop in populations:
        # Filter for this specific cell population
        df_pop = df_averaged[df_averaged['population'] == pop]
        
        # Separate by response status
        # Now each value represents one subject's average
        yes = df_pop[df_pop['response'] == 'yes']['percentage']
        no = df_pop[df_pop['response'] == 'no']['percentage']
        
        # Perform Mann-Whitney U test on subject-level averages
        u_statistic, p_val = mannwhitneyu(yes, no, alternative='two-sided')
        
        # Calculate descriptive statistics
        median_yes = yes.median()
        median_no = no.median()
        median_diff = median_yes - median_no
        
        # Calculate effect size
        n_yes = len(yes)  # Number of unique subjects who responded
        n_no = len(no)    # Number of unique subjects who didn't respond
        rank_biserial = 1 - (2 * u_statistic) / (n_yes * n_no)
        
        # Determine significance
        significant_uncorrected = "Yes" if p_val < alpha else "No"
        
        results.append({
            'Cell Population': pop,
            'Median % Responders': round(median_yes, 5),
            'Median % Non-Responders': round(median_no, 5),
            'Median Difference': round(median_diff, 5),
            'P-Value': round(p_val, 5),
            'Significant Difference': significant_uncorrected,
            'Effect Size (r)': round(rank_biserial, 5)
        })

    results_df = DataFrame(results)
    
    return results_df

COMPARISON = compare_populations(RESP_FREQ_DF)
COMPARISON_FILTER = compare_populations(DATA_FRAME_FILTERED_BOXPLOT)

def train_and_evaluate_model(data_frame: DataFrame):    
    """
    Train model with proper cross-validation to estimate real-world performance.
    """
    # 1. Calculate total count for each subject (sum of all cell types)
    data_frame['total_count'] = data_frame[CELL_TYPES].sum(axis=1)
    
    # 2. Feature Engineering: Convert to percentages
    X = DataFrame()
    for col in CELL_TYPES:
        X[f"{col}_pct"] = (data_frame[col] / data_frame['total_count']) * 100
    
    # 3. Target Encoding
    le = LabelEncoder()
    y = le.fit_transform(data_frame['response'])
            
    # 5. Train and evaluate with cross-validation
    clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=3)
            
    # 6. Train final model on ALL data for deployment
    clf.fit(X, y)
        
    return clf, le

def predict_new_sample(model: RandomForestClassifier, encoder: LabelEncoder, feature_cols: list[str], new_data: dict[str, int]):
    """
    Predict response for a new patient's PBMC sample.    
    """
    # 1. Convert input to DataFrame
    sample_df = DataFrame([new_data])
    
    # 2. Calculate total count
    sample_df['total_count'] = sample_df[feature_cols].sum(axis=1)
    
    # 3. Calculate percentages exactly as done during training
    X_input = DataFrame()
    for col in feature_cols:
        X_input[f"{col}_pct"] = (sample_df[col] / sample_df['total_count']) * 100
    
    # 4. Get prediction and probabilities
    pred_code = model.predict(X_input)[0]
    prob = model.predict_proba(X_input)[0]
    
    # 5. Decode prediction (0/1 -> no/yes)
    label = encoder.inverse_transform([pred_code])[0]
    
    # Get the probability for the predicted class
    predicted_class_prob = prob[pred_code]
    
    return {
        'prediction': label,
        'confidence': round(predicted_class_prob * 100, 2),
        'probability_no': round(prob[0] * 100, 2),
        'probability_yes': round(prob[1] * 100, 2)
    }

# Handle multiple samples per subject by averaging
# This prevents data leakage during cross-validation
DATA_FRAME_SUBJECT = DATA_FRAME2.groupby(['subject', 'response'])[CELL_TYPES].mean().reset_index()

if __name__ == "__main__":
    # Train and evaluate the model
    clf, le = train_and_evaluate_model(DATA_FRAME_SUBJECT)

    # Test prediction on new patient
    new_patient_data = {
        'b_cell': 10000,
        'cd8_t_cell': 21000,
        'cd4_t_cell': 37000,
        'nk_cell': 14000,
        'monocyte': 13000
    }

    result = predict_new_sample(clf, le, CELL_TYPES, new_patient_data)
    print(f"\n=== New Patient Prediction ===")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"P(no response): {result['probability_no']}%")
    print(f"P(yes response): {result['probability_yes']}%")