#Author: Jack W.

class CalorieGoalCalculator:
  def __init__(self, height_cm, weight_kg, age, gender, goal):
      self.height_cm = height_cm
      self.weight_kg = weight_kg
      self.age = age
      self.gender = gender
      self.goal = goal  # 'lose', 'maintain', or 'gain' weight

  def calculate_calorie_goal(self):
      # Basal Metabolic Rate (BMR) calculation based on Harris-Benedict equation
      if self.gender == 'male':
          bmr = 88.362 + (13.397 * self.weight_kg) + (4.799 * self.height_cm) - (5.677 * self.age)
      else:
          bmr = 447.593 + (9.247 * self.weight_kg) + (3.098 * self.height_cm) - (4.330 * self.age)

      # Apply activity level multiplier (adjust as needed)
      if self.goal == 'lose':
          calorie_goal = bmr * 1.2  # Sedentary (little or no exercise)
      elif self.goal == 'maintain':
          calorie_goal = bmr * 1.375  # Lightly active (light exercise or sports 1-3 days a week)
      elif self.goal == 'gain':
          calorie_goal = bmr * 1.55  # Moderately active (moderate exercise or sports 3-5 days a week)

      return calorie_goal

# Example usage:
if __name__ == "__main__":
  height_cm = float(input("Enter your height in centimeters: "))
  weight_kg = float(input("Enter your weight in kilograms: "))
  age = int(input("Enter your age: "))
  gender = input("Enter your gender (male or female): ").lower()
  goal = input("Enter your weight goal (lose, maintain, or gain): ").lower()

  calculator = CalorieGoalCalculator(height_cm, weight_kg, age, gender, goal)
  calorie_goal = calculator.calculate_calorie_goal()
  print(f"Your daily calorie intake goal is approximately {calorie_goal} calories.")
