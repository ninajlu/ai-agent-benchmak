from flask import Flask, render_template, request
from experiments.leaderboard import Leaderboard, AgentCategory

app = Flask(__name__)
leaderboard = Leaderboard()

@app.route("/")
def index():
    # Show overview of all categories
    categories = [category for category in AgentCategory]
    category_rankings = {
        category: leaderboard.get_rankings(category)[:3]  # Top 3 per category
        for category in categories
    }
    return render_template("index.html", category_rankings=category_rankings)

@app.route("/leaderboard/<category>")
def category_leaderboard(category):
    try:
        category_enum = AgentCategory(category)
        rankings = leaderboard.get_rankings(category_enum)
        return render_template(
            "category_leaderboard.html",
            category=category_enum,
            rankings=rankings
        )
    except ValueError:
        return "Invalid category", 404 