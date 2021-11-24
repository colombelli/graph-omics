:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///clin_proc.csv" AS row
MERGE (patient:Patient {patientId: row.id})
SET patient.tumor_tissue_site = row.tumor_tissue_site
SET patient.years_to_birth = row.years_to_birth
SET patient.vital_status = row.vital_status
SET patient.days_to_death = row.days_to_death
SET patient.days_to_last_followup = row.days_to_last_followup
SET patient.pathologic_stage = row.pathologic_stage
SET patient.pathology_T_stage = row.pathology_T_stage
SET patient.pathology_N_stage = row.pathology_N_stage
SET patient.pathology_M_stage = row.pathology_M_stage
SET patient.gender = row.gender
SET patient.date_of_initial_pathologic_diagnosis = row.date_of_initial_pathologic_diagnosis
SET patient.radiation_therapy = row.radiation_therapy
SET patient.histological_type = row.histological_type
SET patient.number_pack_years_smoked = row.number_pack_years_smoked
SET patient.year_of_tobacco_smoking_onset = row.year_of_tobacco_smoking_onset
SET patient.ethnicity = row.ethnicity