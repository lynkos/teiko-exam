import pandas
import scipy.stats as stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sqlite3 import connect
from data_analysis import SUMMARY_TABLE_NAME, DATABASE, CELL_TYPES

connection = connect(DATABASE)

# Summary table
DATA_FRAME_SUMMARY = pandas.read_sql_query(
    f"""SELECT sample, total_count AS 'Total Count', population, count, percentage
        FROM {SUMMARY_TABLE_NAME}
    """, connection
)

# Population relative frequencies comparing responders
# versus non-responders using a boxplot for each
# immune cell population
DATA_FRAME = pandas.read_sql_query(
    f"""SELECT s.population, s.percentage, subj.response
        FROM {SUMMARY_TABLE_NAME} s
        JOIN samples t ON s.sample = t.sample
        JOIN subjects subj ON t.subject = subj.subject
        WHERE subj.response IN ('yes', 'no')
    """, connection
)

# Population relative frequencies comparing responders
# versus non-responders using a boxplot for each
# immune cell population
DATA_FRAME_FILTERED_BOXPLOT = pandas.read_sql_query(
    f"""SELECT s.population, s.percentage, subj.response
        FROM {SUMMARY_TABLE_NAME} s
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
DATA_FRAME2 = pandas.read_sql_query(
    f"""SELECT DISTINCT s.sample, s.total_count, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, t.subject, subj.response
        FROM {SUMMARY_TABLE_NAME} s
        JOIN samples t ON s.sample = t.sample
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
        AND subj.response IN ('yes', 'no')
    """, connection
)

connection.close()

# TEST
def compare_populations(input_df = DATA_FRAME_FILTERED_BOXPLOT):
    """
    Compare cell populations between responders and non-responders
    """
    
    populations = input_df['population'].unique()
    results = []
    
    alpha = 0.05

    for pop in populations:
        # Filter for this specific cell population
        df_pop = input_df[input_df['population'] == pop]
        
        # Separate by response status
        # Now each value represents one subject's average
        yes = df_pop[df_pop['response'] == 'yes']['percentage']
        no = df_pop[df_pop['response'] == 'no']['percentage']
        
        # Perform Mann-Whitney U test on subject-level averages
        u_statistic, p_val = stats.mannwhitneyu(yes, no, alternative='two-sided')
        
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
            'Significant': significant_uncorrected,
            'Effect Size (r)': round(rank_biserial, 5)
        })

    results_df = pandas.DataFrame(results)
    
    return results_df

COMPARISON = compare_populations()

def train_model(df):    
    # 1. Feature Engineering (Percentages)
    X = pandas.DataFrame()
    for col in CELL_TYPES:
        X[f"{col}_pct"] = (df[col] / df['total_count']) * 100
    
    # 2. Target Encoding
    le = LabelEncoder()
    y = le.fit_transform(df['response'])

    # 3. Train Classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    clf.fit(X, y)
    
    return clf, le

def predict_new_sample(model, encoder, feature_cols, new_data):
    """
    Takes a dictionary of raw counts and returns a prediction.
    new_data = {'total_count': 100000, 'b_cell': 5000, ...}
    """
    # 1. Convert input to DataFrame
    sample_df = pandas.DataFrame([new_data])
    
    # 2. Calculate percentages exactly as done during training
    X_input = pandas.DataFrame()
    for col in feature_cols:
        X_input[f"{col}_pct"] = (sample_df[col] / sample_df['total_count']) * 100
    
    # 3. Get Prediction
    pred_code = model.predict(X_input)[0]
    prob = model.predict_proba(X_input)[0]
    
    # 4. Decode (0/1 -> no/yes)
    label = encoder.inverse_transform([pred_code])[0]
    
    return {
        'prediction': label,
        'confidence': round(max(prob) * 100, 2)
    }

clf, le = train_model(DATA_FRAME2)

new_patient_data = {
    'total_count': 95000,
    'b_cell': 10000,
    'cd8_t_cell': 21000,
    'cd4_t_cell': 37000,
    'nk_cell': 14000,
    'monocyte': 13000
}

result = predict_new_sample(clf, le, CELL_TYPES, new_patient_data)
print(f"Prediction: {result['prediction']} ({result['confidence']}% confidence)")