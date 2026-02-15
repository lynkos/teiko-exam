import pandas
from sqlite3 import connect
from data_analysis import DATABASE

connection = connect(DATABASE)

# Identify all melanoma PBMC samples at baseline
# (time_from_treatment_start is 0) from patients
# who have been treated with miraclib
DATA_FRAME_FILTER = pandas.read_sql_query(
    f"""SELECT t.sample
        FROM samples t
        JOIN subjects subj ON t.subject = subj.subject
        WHERE t.sample_type = 'PBMC'
        AND t.time_from_treatment_start = 0
        AND subj.condition = 'melanoma'
        AND subj.treatment = 'miraclib'
    """, connection
)

# How many samples from each project
DATA_FRAME_PROJECTS = pandas.read_sql_query(
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

# How many subjects were responders/non-responders 
DATA_FRAME_RESPONDERS = pandas.read_sql_query(
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

# How many subjects were males/females
DATA_FRAME_SEXES = pandas.read_sql_query(
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

connection.close()