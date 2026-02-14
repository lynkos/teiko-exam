import pandas
import scipy.stats as stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sqlite3 import connect
from data_analysis import SUMMARY_TABLE_NAME, DATABASE

CELL_TYPES = [ "b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte" ]

connection = connect(DATABASE)
# FILTER
DATA_FRAME = pandas.read_sql_query(
    f"""SELECT s.sample, s.total_count, s.population, s.count, s.percentage, t.subject, subj.response
        FROM {SUMMARY_TABLE_NAME} s
        JOIN samples t ON s.sample = t.sample
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
        AND subj.response IN ('yes', 'no')
    """, connection
)

DATA_FRAME2 = pandas.read_sql_query(
    f"""SELECT DISTINCT t.sample, s.total_count, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, t.subject, subj.response
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
def compare_populations():
    populations = DATA_FRAME['population'].unique()
    results = []

    for pop in populations:
        df_pop = DATA_FRAME[DATA_FRAME['population'] == pop]
        
        yes = df_pop[df_pop['response'] == 'yes']['percentage']
        no = df_pop[df_pop['response'] == 'no']['percentage']

        _, p_val = stats.mannwhitneyu(yes, no)
        
        results.append({
            'Population': pop,
            'P-Value': round(p_val, 5),
            'Significant (p < 0.05)': p_val < 0.05,
            'Mean_Yes': round(yes.mean(), 2),
            'Mean_No': round(no.mean(), 2)
        })

    return pandas.DataFrame(results)

print(compare_populations())

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