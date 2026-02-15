from pandas import read_sql_query
from sqlite3 import connect
from data_analysis import DATABASE

connection = connect(DATABASE)

# Identify all melanoma PBMC samples at baseline
# (time_from_treatment_start is 0) from patients
# who have been treated with miraclib
DATA_FRAME_FILTER = read_sql_query(
    f"""SELECT t.sample
        FROM samples t
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND t.time_from_treatment_start = 0
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
    """, connection
)
print("1. All melanoma PBMC samples at baseline from patients treated with miraclib:")
print(DATA_FRAME_FILTER)

# How many samples from each project
DATA_FRAME_PROJECTS = read_sql_query(
    f"""SELECT subj.project, COUNT(t.sample) AS 'Number of Samples'
        FROM samples t
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND t.time_from_treatment_start = 0
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
        GROUP BY subj.project
    """, connection
)
print("\n2. Among the previously filtered samples, number of samples from each project:")
print(DATA_FRAME_PROJECTS)

# How many subjects were responders/non-responders 
DATA_FRAME_RESPONDERS = read_sql_query(
    f"""SELECT subj.response, COUNT(DISTINCT t.subject) AS 'Count'
        FROM samples t
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND t.time_from_treatment_start = 0
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
        GROUP BY subj.response
    """, connection
)
print("\n3. Among the previously filtered samples, number of subjects who were responders (yes) vs. non-responders (no):")
print(DATA_FRAME_RESPONDERS)

# How many subjects were males/females
DATA_FRAME_SEXES = read_sql_query(
    f"""SELECT subj.sex, COUNT(DISTINCT t.subject) AS 'Count'
        FROM samples t
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND t.time_from_treatment_start = 0
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
        GROUP BY subj.sex
    """, connection
)
print("\n4. Among the previously filtered samples, number of subjects who were males (M) vs females (F):")
print(DATA_FRAME_SEXES)

# Get number of b_cells for all males AND melanoma AND t = 0 AND responds
DF = read_sql_query(
    f"""SELECT t.b_cell
        FROM samples t
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.time_from_treatment_start = 0
        AND subj.condition = 'melanoma'
        AND subj.sex = 'M'
        AND subj.response = 'yes'
    """, connection
)

avg_b_cells = DF['b_cell'].mean()
print("\n5. Average number of B cells for Melanoma males responders at time = 0:", avg_b_cells)

connection.close()