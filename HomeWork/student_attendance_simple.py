import os
import pandas as pd

# Read the Excel file
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "attendance.xlsx")

df = pd.read_excel(file_path)

print("1. First 5 rows of the dataset")
print(df.head())

print("\n2. Shape of the dataset")
print(df.shape)

print("\n3. Column names")
print(df.columns.tolist())

print("\n4. Missing values in each column")
print(df.isnull().sum())

# Replace 'Never' with missing value for Last Present Date
# Then convert the column to datetime
print("\n5. Clean the 'Last Present Date' column")
df["Last Present Date"] = df["Last Present Date"].replace("Never", pd.NA)
df["Last Present Date"] = pd.to_datetime(df["Last Present Date"], errors="coerce")
print(df[["Student Name", "Last Present Date"]].head())

# Rename columns to snake_case
print("\n6. Rename columns")
df = df.rename(columns={
    "Roll No": "roll_no",
    "Student Name": "student_name",
    "Total Classes": "total_classes",
    "Attendance %": "attendance_pct",
    "Last Present Date": "last_present_date",
    "Consecutive Absences": "consecutive_absences",
    "Classes Needed (75%)": "classes_needed_75_pct",
})
print(df.columns.tolist())

# Convert attendance percentage to numeric value
print("\n7. Convert Attendance % to number")
df["attendance_pct"] = df["attendance_pct"].str.replace("%", "", regex=False)
df["attendance_pct"] = pd.to_numeric(df["attendance_pct"], errors="coerce") / 100
print(df[["student_name", "attendance_pct"]].head())

# Filter Critical students
print("\n8. Students with Critical status")
critical_students = df[df["Status"] == "Critical"].sort_values("attendance_pct")
print(critical_students[["roll_no", "student_name", "attendance_pct", "Status"]].head(10))

# Group by status
print("\n9. Summary by status")
status_summary = df.groupby("Status").agg(
    total_students=("roll_no", "count"),
    average_attendance=("attendance_pct", "mean"),
    max_absences=("consecutive_absences", "max")
)
print(status_summary)

# Risk score
print("\n10. Top 10 students by risk score")
df["risk_score"] = (df["Absent"] * 0.4) + (df["consecutive_absences"] * 0.6)
top_10 = df.sort_values("risk_score", ascending=False).head(10)
print(top_10[["roll_no", "student_name", "risk_score"]])

# Save output files
print("\n11. Save files")
critical_students.to_csv(os.path.join(base_dir, "critical_students.csv"), index=False)
status_summary.to_csv(os.path.join(base_dir, "attendance_summary_by_status.csv"))
top_10[["roll_no", "student_name", "risk_score"]].to_csv(os.path.join(base_dir, "top_10_students_by_risk_score.csv"), index=False)

print("Files created successfully.")
