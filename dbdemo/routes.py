from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import app, db  ## initially created by __init__.py, need to be used here
import json

@app.route("/")
def index():
    try:
        ## create connection to database
        cur = db.connection.cursor()
        ## execute query
        cur.execute("SELECT g.grade, s.first_name, s.last_name FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'DRI' ORDER BY g.grade DESC LIMIT 1")
        ## cursor.fetchone() does not return the column names, only the row values
        ## thus we manually create a mapping between the two, the dictionary res
        column_names = [i[0] for i in cur.description]
        res = dict(zip(column_names, cur.fetchone()))
        best_dribbling_grade = res.get("grade")
        best_dribbler = res.get("first_name") + " " + res.get("last_name")

        cur.execute("SELECT g.grade, s.first_name, s.last_name FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'SHO' ORDER BY g.grade DESC LIMIT 1")
        res = dict(zip(column_names, cur.fetchone()))
        cur.close()
        best_shooting_grade = res.get("grade")
        best_shooter = res.get("first_name") + " " + res.get("last_name")

        return render_template("landing.html",
                               pageTitle="Landing Page",
                               best_dribbling_grade=best_dribbling_grade,
                               best_dribbler=best_dribbler,
                               best_shooting_grade=best_shooting_grade,
                               best_shooter=best_shooter)
    except Exception as e:
        print(e)
        return render_template("landing.html", pageTitle="Landing Page")


@app.route("/reviews")
def showReviews():
    try:
        cur = db.connection.cursor()
        cur.execute("""
            SELECT pr.id, s.first_name, s.last_name, pr.manager_name, pr.review_text
            FROM player_reviews pr
            INNER JOIN students s ON pr.student_id = s.id
            ORDER BY pr.id
        """)
        data = cur.fetchall()
        cur.close()
        return render_template("showReviews.html",
                               pageTitle="Player Reviews",
                               data=data)
    except Exception as e:
        print(e)
        return render_template("showReviews.html",
                               pageTitle="Player Reviews",
                               data=[])

SIMILARITY_QUERIES = {
    "pacey_winger": {
        "label": "Fast winger with dribbling and acceleration",
        "vector": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "creative_playmaker": {
        "label": "Creative midfielder with vision and passing",
        "vector": [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "target_striker": {
        "label": "Strong striker with aerial ability and finishing",
        "vector": [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "ball_winner": {
        "label": "Aggressive ball-winning midfielder",
        "vector": [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "ball_playing_cb": {
        "label": "Ball-playing centre-back for build-up",
        "vector": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    },
    "sweeper_keeper": {
        "label": "Goalkeeper comfortable in build-up and off the line",
        "vector": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    }
}

def pad_to_384(v):
    return v + [0.0] * (384 - len(v))

@app.route("/similarity", methods=["GET", "POST"])
def similarity():
    selected_key = None
    results = []

    if request.method == "POST":
        selected_key = request.form.get("query_key")

        if selected_key in SIMILARITY_QUERIES:
            query_vec = pad_to_384(SIMILARITY_QUERIES[selected_key]["vector"])
            query_vec_json = json.dumps(query_vec)

            cur = db.connection.cursor()
            cur.execute("""
                SELECT
                    s.first_name,
                    s.last_name,
                    pr.manager_name,
                    pr.review_text,
                    ROUND(VEC_DISTANCE_COSINE(pr.embedding, VEC_FromText(%s)), 6) AS distance,
                    LEFT(VEC_ToText(pr.embedding), 120) AS embedding_preview
                FROM player_reviews pr
                INNER JOIN students s ON pr.student_id = s.id
                WHERE pr.embedding IS NOT NULL
                ORDER BY VEC_DISTANCE_COSINE(pr.embedding, VEC_FromText(%s)) ASC
                LIMIT 5
            """, (query_vec_json, query_vec_json))
            results = cur.fetchall()
            cur.close()

    return render_template(
        "similarity.html",
        pageTitle="Similarity Search",
        query_options=SIMILARITY_QUERIES,
        selected_key=selected_key,
        results=results
    )


@app.route("/similarity/review/<int:review_id>")
def similarity_from_review(review_id):
    try:
        cur = db.connection.cursor()

        cur.execute("""
            SELECT
                s.first_name,
                s.last_name,
                pr.manager_name,
                pr.review_text,
                LEFT(VEC_ToText(pr.embedding), 120) AS embedding_preview
            FROM player_reviews pr
            INNER JOIN students s ON pr.student_id = s.id
            WHERE pr.id = %s
        """, (review_id,))
        source_review = cur.fetchone()

        if source_review is None:
            cur.close()
            abort(404)

        cur.execute("""
            SELECT
                pr.id,
                s.first_name,
                s.last_name,
                pr.manager_name,
                pr.review_text,
                ROUND(VEC_DISTANCE_COSINE(
                    pr.embedding,
                    (SELECT embedding FROM player_reviews WHERE id = %s)
                ), 6) AS distance,
                LEFT(VEC_ToText(pr.embedding), 120) AS embedding_preview
            FROM player_reviews pr
            INNER JOIN students s ON pr.student_id = s.id
            WHERE pr.id <> %s
              AND pr.embedding IS NOT NULL
            ORDER BY VEC_DISTANCE_COSINE(
                pr.embedding,
                (SELECT embedding FROM player_reviews WHERE id = %s)
            ) ASC
            LIMIT 5
        """, (review_id, review_id, review_id))

        results = cur.fetchall()
        cur.close()

        return render_template(
            "similarity_from_review.html",
            pageTitle="Similarity From Review",
            review_id=review_id,
            source_review=source_review,
            results=results
        )

    except Exception as e:
        print(e)
        return render_template(
            "similarity_from_review.html",
            pageTitle="Similarity From Review",
            review_id=review_id,
            source_review=None,
            results=[]
        )
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle="Not Found"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle="Internal Server Error"), 500