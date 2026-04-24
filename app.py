from __future__ import annotations

import random
from flask import Flask, jsonify, render_template

app = Flask(__name__)

MAX_BALLS = 12
OUTCOME_POOL = [0, 1, 2, 3, 4, 6, "OUT"]


def initial_state() -> dict[str, int | bool]:
    return {
        "score": 0,
        "balls": 0,
        "is_out": False,
        "game_over": False,
    }


game_state = initial_state()


def shot_message(outcome: int | str) -> str:
    if outcome == "OUT":
        return "OUT! Batter is gone."
    if outcome == 0:
        return "Dot ball. No run."
    if outcome == 4:
        return "Great Shot! 4 runs!"
    if outcome == 6:
        return "Massive hit! 6 runs!"
    return f"Nice! {outcome} run{'s' if outcome != 1 else ''}."


@app.route("/")
def home():
    return render_template("index.html", max_balls=MAX_BALLS, state=game_state)


@app.route("/play", methods=["POST"])
def play():
    if game_state["game_over"]:
        return jsonify(
            {
                "message": "Game already ended. Press Reset Game to start again.",
                "score": game_state["score"],
                "balls": game_state["balls"],
                "max_balls": MAX_BALLS,
                "game_over": game_state["game_over"],
                "is_out": game_state["is_out"],
            }
        )

    outcome = random.choice(OUTCOME_POOL)
    game_state["balls"] += 1

    if outcome == "OUT":
        game_state["is_out"] = True
        game_state["game_over"] = True
        message = shot_message(outcome)
    else:
        game_state["score"] += outcome
        message = shot_message(outcome)

    if game_state["balls"] >= MAX_BALLS and not game_state["game_over"]:
        game_state["game_over"] = True
        message = f"{message} Innings complete: {MAX_BALLS} balls done."

    return jsonify(
        {
            "outcome": outcome,
            "message": message,
            "score": game_state["score"],
            "balls": game_state["balls"],
            "max_balls": MAX_BALLS,
            "game_over": game_state["game_over"],
            "is_out": game_state["is_out"],
        }
    )


@app.route("/reset", methods=["POST"])
def reset():
    game_state.clear()
    game_state.update(initial_state())
    return jsonify(
        {
            "message": "Game reset. Ready for the next innings!",
            "score": game_state["score"],
            "balls": game_state["balls"],
            "max_balls": MAX_BALLS,
            "game_over": game_state["game_over"],
            "is_out": game_state["is_out"],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
