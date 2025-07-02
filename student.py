import pandas as pd
import os

class StudentManager:
    def __init__(self, csv_path="student.csv"):
        self.csv_path = csv_path
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
        else:
            self.df = pd.DataFrame(columns=[
                "student_id", "name", "interests", "total_required_credits", "earned_credits"
            ])

    def add_student_from_input(self):
        print("=== 学生情報を入力してください ===")
        student_id = input("学籍番号: ")
        name = input("名前: ")
        print("興味分野（カンマ区切りで複数入力可）")
        interests_input = input("例：物理学,AI,留学: ")
        interests = [s.strip() for s in interests_input.split(",")]

        try:
            total_required_credits = int(input("必要単位数（例：124）: "))
            earned_credits = int(input("取得済み単位数（例：90）: "))
        except ValueError:
            print("単位数は整数で入力してください。")
            return

        new_student = {
            "student_id": student_id,
            "name": name,
            "interests": ";".join(interests),
            "total_required_credits": total_required_credits,
            "earned_credits": earned_credits
        }

        self.df = pd.concat([self.df, pd.DataFrame([new_student])], ignore_index=True)
        self.save()
        print("✅ 学生を追加しました。")

    def save(self):
        self.df.to_csv(self.csv_path, index=False)

    def show_all(self):
        print(self.df)


if __name__ == "__main__":
    manager = StudentManager("student.csv")
    manager.add_student_from_input()
    print("\n=== 現在の学生一覧 ===")
    manager.show_all()
