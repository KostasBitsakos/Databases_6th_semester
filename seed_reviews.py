import os
import random
from faker import Faker
import MySQLdb

fake = Faker()
random.seed(42)
Faker.seed(42)

DB_HOST = os.getenv("MYSQL_HOST", "db")
DB_USER = os.getenv("MYSQL_USER", "demo_user")
DB_PASS = os.getenv("MYSQL_PASSWORD", "demo_pass")
DB_NAME = os.getenv("MYSQL_DB", "demo")

ARCHETYPES = [
    {
        "name": "pacey winger",
        "grade_ranges": {"PAC": (85, 99), "SHO": (65, 85), "PAS": (68, 84), "DRI": (82, 98), "DEF": (25, 55), "PHY": (55, 78)},
        "openings": [
            "Direct wide attacker with elite acceleration.",
            "Quick winger who immediately threatens space.",
            "Explosive flank player who can isolate defenders.",
            "Dynamic winger with outstanding speed over short distances."
        ],
        "strengths_1": [
            "Very dangerous in one versus one situations.",
            "Creates separation easily with his first steps.",
            "Beats defenders consistently when receiving wide.",
            "Can destabilize full-backs with sharp changes of direction."
        ],
        "strengths_2": [
            "Carries the ball effectively in transition.",
            "Adds value through dribbling and progressive runs.",
            "Attacks the outside channel with intent.",
            "Provides width and pushes the defensive line backwards."
        ],
        "tactical": [
            "Best used in systems that create space in wide areas.",
            "More effective when the team plays vertically.",
            "Particularly useful against stretched defensive lines.",
            "Thrives when he can receive early and attack open grass."
        ],
        "weaknesses": [
            "Final decision in crowded areas can still improve.",
            "Less influential when forced to play with his back to goal.",
            "Can be reduced when the game becomes very compact centrally.",
            "His impact drops slightly when he receives fewer transition opportunities."
        ],
    },
    {
        "name": "creative playmaker",
        "grade_ranges": {"PAC": (55, 78), "SHO": (60, 82), "PAS": (85, 99), "DRI": (78, 94), "DEF": (35, 62), "PHY": (50, 75)},
        "openings": [
            "Creative midfielder with excellent vision and passing range.",
            "Inventive playmaker who connects midfield and attack.",
            "Technical creator with high-level awareness in possession.",
            "Attacking midfielder who sees forward options very early."
        ],
        "strengths_1": [
            "Finds runners between the lines with consistency.",
            "Can control tempo and improve circulation.",
            "Offers smart passing choices under moderate pressure.",
            "Helps unlock compact structures with precise distribution."
        ],
        "strengths_2": [
            "Comfortable receiving in advanced pockets.",
            "Adds value through combination play and progression.",
            "Can shape the attacking rhythm of the team.",
            "Produces quality final balls when facing organized blocks."
        ],
        "tactical": [
            "Best in systems that value controlled possession.",
            "Useful when the team needs a central creator.",
            "Particularly effective when surrounded by mobile runners.",
            "Works well when given freedom between midfield and attack."
        ],
        "weaknesses": [
            "Not the most intense profile defensively.",
            "Can be less effective in highly physical matches.",
            "Defensive coverage is not his primary contribution.",
            "Needs nearby movement to maximize his creative output."
        ],
    },
    {
        "name": "target striker",
        "grade_ranges": {"PAC": (45, 72), "SHO": (82, 97), "PAS": (45, 68), "DRI": (52, 75), "DEF": (20, 45), "PHY": (82, 98)},
        "openings": [
            "Strong centre forward with reliable finishing and aerial presence.",
            "Physical striker who can lead the line centrally.",
            "Penalty-box attacker with very good presence in duels.",
            "Classic number nine profile with strength and finishing."
        ],
        "strengths_1": [
            "Holds up the ball effectively under pressure.",
            "Competes well against central defenders physically.",
            "Provides a strong target for direct play.",
            "Attacks crosses with conviction and timing."
        ],
        "strengths_2": [
            "Dangerous when the team delivers early balls into the area.",
            "Useful as a reference point in the final third.",
            "Can stabilize attacks by securing first contact.",
            "Offers consistent threat in the box."
        ],
        "tactical": [
            "Best used in systems that generate crosses or direct service.",
            "More effective when supported by runners around him.",
            "Useful in matches that require territory and central occupation.",
            "Works well when the team can play into him early."
        ],
        "weaknesses": [
            "Not the most dynamic profile in open transition.",
            "Ball carrying over longer distances is limited.",
            "Less suited to highly fluid wide rotations.",
            "Contribution outside the box is more functional than creative."
        ],
    },
    {
        "name": "pressing forward",
        "grade_ranges": {"PAC": (72, 90), "SHO": (72, 90), "PAS": (58, 76), "DRI": (68, 86), "DEF": (35, 62), "PHY": (70, 88)},
        "openings": [
            "Energetic attacker with strong pressing habits.",
            "Mobile striker who contributes heavily without the ball.",
            "Work-rate driven forward with direct attacking intent.",
            "High-intensity front player suited to aggressive systems."
        ],
        "strengths_1": [
            "Can force mistakes through pressure on defenders.",
            "Attacks space quickly after regains.",
            "Helps lead the first defensive line effectively.",
            "Maintains high involvement across transitions."
        ],
        "strengths_2": [
            "Combines mobility with useful attacking runs.",
            "Adds value through intensity and repeated sprints.",
            "Capable of disrupting build-up patterns.",
            "Can create attacking moments from defensive work."
        ],
        "tactical": [
            "Best in teams that want to defend high.",
            "Useful in transition-heavy matches.",
            "Particularly effective when the front line presses collectively.",
            "Fits systems that value intensity over slow buildup."
        ],
        "weaknesses": [
            "May lose efficiency in slower positional attacks.",
            "Refinement in tight-space link play can still improve.",
            "Can become less influential when pressing triggers are unclear.",
            "Not always the cleanest final-third technician."
        ],
    },
    {
        "name": "ball-winning midfielder",
        "grade_ranges": {"PAC": (58, 80), "SHO": (40, 68), "PAS": (60, 80), "DRI": (55, 76), "DEF": (82, 97), "PHY": (78, 95)},
        "openings": [
            "Defensive midfielder with strong ball recovery habits.",
            "Aggressive central midfielder focused on winning duels.",
            "Midfield destroyer profile with reliable defensive output.",
            "Combative midfielder who protects central zones well."
        ],
        "strengths_1": [
            "Reads loose balls and second contacts effectively.",
            "Covers ground with intensity and purpose.",
            "Provides strong tackling and interruption value.",
            "Helps stabilize the team out of possession."
        ],
        "strengths_2": [
            "Competes consistently in physical midfield battles.",
            "Can recover possession and restart play simply.",
            "Offers balance to more attack-minded teammates.",
            "Supports compact defensive structures well."
        ],
        "tactical": [
            "Best in systems that need midfield protection.",
            "Useful when the team wants more control without the ball.",
            "Particularly effective in compact or medium blocks.",
            "Fits lineups that need a dedicated recovery specialist."
        ],
        "weaknesses": [
            "Final-third creativity is limited.",
            "Can be less progressive in advanced possession phases.",
            "Ball progression is usually functional rather than incisive.",
            "Does not naturally offer much attacking flair."
        ],
    },
    {
        "name": "deep-lying playmaker",
        "grade_ranges": {"PAC": (48, 72), "SHO": (45, 70), "PAS": (84, 98), "DRI": (68, 86), "DEF": (62, 84), "PHY": (58, 80)},
        "openings": [
            "Deep midfielder who dictates circulation from lower zones.",
            "Regista-style player with calm possession habits.",
            "Playmaking pivot who supports the build-up phase.",
            "Deep creator who organizes rhythm and progression."
        ],
        "strengths_1": [
            "Distributes the ball with consistency and range.",
            "Can break lines with measured passing choices.",
            "Helps the team progress through patient control.",
            "Remains composed when orchestrating from deep."
        ],
        "strengths_2": [
            "Offers structure to the first phase of possession.",
            "Scans well before receiving and selects safe forward options.",
            "Provides balance between positioning and passing.",
            "Supports tempo management during sustained possession."
        ],
        "tactical": [
            "Best in teams that want to build from the back.",
            "Useful against compact structures that require circulation.",
            "Particularly effective when central positioning is important.",
            "Fits systems that rely on a stable deep distributor."
        ],
        "weaknesses": [
            "Does not offer major running power in open games.",
            "May struggle when matches become too stretched physically.",
            "Acceleration is not a major part of his profile.",
            "Needs teammates who move intelligently ahead of him."
        ],
    },
    {
        "name": "overlapping full-back",
        "grade_ranges": {"PAC": (78, 94), "SHO": (42, 68), "PAS": (68, 86), "DRI": (72, 88), "DEF": (68, 84), "PHY": (70, 88)},
        "openings": [
            "Dynamic full-back with strong pace and stamina.",
            "Attack-minded wide defender who adds width.",
            "Modern full-back who supports advanced phases regularly.",
            "Energetic flank defender with clear offensive contribution."
        ],
        "strengths_1": [
            "Provides reliable overlaps and recovery runs.",
            "Supports combinations on the outside effectively.",
            "Carries the ball forward with purpose.",
            "Can contribute useful service from advanced areas."
        ],
        "strengths_2": [
            "Gives the team width and running power.",
            "Helps progression by moving the game up the flank.",
            "Maintains activity across both phases.",
            "Has enough pace to recover after forward movements."
        ],
        "tactical": [
            "Best in systems where full-backs are encouraged to advance.",
            "Useful when the winger moves inside and leaves space outside.",
            "Fits teams that want constant wide support.",
            "Particularly effective when width must come from the back line."
        ],
        "weaknesses": [
            "Can leave space behind if the structure is poor.",
            "Needs defensive balance around him when pushing high.",
            "Risk management in advanced positioning still matters.",
            "Final action quality can vary under pressure."
        ],
    },
    {
        "name": "defensive full-back",
        "grade_ranges": {"PAC": (68, 86), "SHO": (30, 55), "PAS": (55, 74), "DRI": (50, 70), "DEF": (80, 94), "PHY": (74, 90)},
        "openings": [
            "Reliable full-back focused on defensive stability.",
            "Wide defender who prioritizes structure and coverage.",
            "Defensive-minded flank player with disciplined positioning.",
            "Balanced full-back profile built around solidity."
        ],
        "strengths_1": [
            "Defends his channel with concentration and discipline.",
            "Wins a good share of direct wide duels.",
            "Maintains compact distances with the back line.",
            "Provides secure coverage rather than risky progression."
        ],
        "strengths_2": [
            "Useful in protecting the weak side and far-post areas.",
            "Offers dependable defensive behavior across phases.",
            "Can stabilize teams that need stronger flank defending.",
            "Supports conservative game plans effectively."
        ],
        "tactical": [
            "Best in systems that value defensive balance.",
            "Useful when the opposite side attacks more aggressively.",
            "Fits teams that defend crosses and wide entries often.",
            "Particularly effective against dangerous wingers."
        ],
        "weaknesses": [
            "Final-third contribution is limited.",
            "Does not naturally provide major attacking width.",
            "Can be less progressive with the ball than modern attacking full-backs.",
            "Crossing and dribbling are secondary parts of his role."
        ],
    },
    {
        "name": "ball-playing centre-back",
        "grade_ranges": {"PAC": (58, 78), "SHO": (30, 52), "PAS": (72, 90), "DRI": (55, 74), "DEF": (82, 96), "PHY": (78, 94)},
        "openings": [
            "Centre-back with strong distribution and calm build-up play.",
            "Technical defender who contributes to progression from the back.",
            "Composed central defender suited to possession structures.",
            "Ball-playing defender with useful passing range."
        ],
        "strengths_1": [
            "Can break lines with measured passes.",
            "Remains composed when pressured in the first phase.",
            "Helps sustain clean circulation from deeper zones.",
            "Offers more than simple clearance-only defending."
        ],
        "strengths_2": [
            "Supports possession-heavy teams with secure distribution.",
            "Adds value in buildup without losing defensive focus.",
            "Finds midfield connections reliably from the back line.",
            "Can initiate attacks through thoughtful passing."
        ],
        "tactical": [
            "Best in teams that want to construct from deep.",
            "Useful when build-up quality from the back is important.",
            "Fits systems that demand technical defenders.",
            "Particularly effective in controlled possession models."
        ],
        "weaknesses": [
            "May be tested in very direct physical battles.",
            "Defensive play is stronger when the structure around him is clear.",
            "Pure recovery speed is not his standout trait.",
            "Can be exposed if asked to defend too much open space repeatedly."
        ],
    },
    {
        "name": "physical centre-back",
        "grade_ranges": {"PAC": (48, 72), "SHO": (25, 45), "PAS": (45, 68), "DRI": (38, 58), "DEF": (84, 98), "PHY": (86, 99)},
        "openings": [
            "Strong central defender with dominant physical presence.",
            "Robust centre-back built for duels and aerial defending.",
            "Powerful defender who protects the box aggressively.",
            "Traditional central defender with strength and authority."
        ],
        "strengths_1": [
            "Attacks crosses with confidence and force.",
            "Competes very well in direct physical battles.",
            "Helps defend the penalty area with authority.",
            "Provides strong resistance against target forwards."
        ],
        "strengths_2": [
            "Useful in teams that defend deeper and face many deliveries.",
            "Can clear danger consistently under pressure.",
            "Wins a high share of aerial contacts.",
            "Adds security in defensive set-piece situations."
        ],
        "tactical": [
            "Best in direct or low-block defensive contexts.",
            "Useful when box defending is a priority.",
            "Particularly effective against physical attackers.",
            "Fits systems that value duels, clearances, and structure."
        ],
        "weaknesses": [
            "Passing contribution is more basic than expansive.",
            "Not ideal for heavily possession-based buildup roles.",
            "Can be less comfortable in highly open defensive races.",
            "Ball progression is not the main source of his value."
        ],
    },
    {
        "name": "shot-stopping goalkeeper",
        "grade_ranges": {"PAC": (20, 40), "SHO": (10, 30), "PAS": (45, 70), "DRI": (20, 40), "DEF": (35, 60), "PHY": (60, 85)},
        "openings": [
            "Goalkeeper with strong reflexes and reliable shot-stopping.",
            "Reactive keeper profile built around saves.",
            "Traditional goalkeeper who protects the goal effectively.",
            "Keeper who adds value primarily through stopping shots."
        ],
        "strengths_1": [
            "Handles close-range situations with composure.",
            "Can make difficult saves from compact distances.",
            "Provides security on the line during defensive phases.",
            "Responds well when the team faces sustained pressure."
        ],
        "strengths_2": [
            "Useful in systems that concede shooting volume.",
            "Offers reassurance through core goalkeeping fundamentals.",
            "Can keep the team competitive through interventions.",
            "Best when his primary task is direct shot prevention."
        ],
        "tactical": [
            "Best in teams that defend closer to their own goal.",
            "Useful when the defensive block is deeper.",
            "Fits setups that prioritize traditional goal protection.",
            "Particularly effective when the box must be defended repeatedly."
        ],
        "weaknesses": [
            "Distribution is less influential than his saving ability.",
            "Not the most proactive profile outside the area.",
            "Build-up contribution is relatively limited.",
            "Less suited to very aggressive sweeping roles."
        ],
    },
    {
        "name": "sweeper keeper",
        "grade_ranges": {"PAC": (25, 45), "SHO": (10, 30), "PAS": (68, 88), "DRI": (25, 45), "DEF": (35, 60), "PHY": (60, 82)},
        "openings": [
            "Goalkeeper comfortable outside the box and useful in buildup.",
            "Modern keeper profile with proactive positioning.",
            "Sweeper-keeper who helps the team in possession.",
            "Ball-playing goalkeeper suited to higher defensive lines."
        ],
        "strengths_1": [
            "Supports circulation with calmer distribution.",
            "Can cover space behind the defense more actively.",
            "Offers an extra passing option in early buildup.",
            "Provides value through proactive defensive positioning."
        ],
        "strengths_2": [
            "Useful in teams that defend high and want clean exits.",
            "Adds stability when the back line leaves space behind.",
            "Can help connect the first phase under light pressure.",
            "Contributes beyond pure shot-stopping situations."
        ],
        "tactical": [
            "Best in possession-oriented systems with aggressive field position.",
            "Useful when the team needs support behind a high line.",
            "Fits modern structures that use the goalkeeper in buildup.",
            "Particularly effective when proactive positioning is required."
        ],
        "weaknesses": [
            "May take more risk than a traditional goalkeeper profile.",
            "Needs strong decision-making under pressure.",
            "Pure line goalkeeping can be less defining than his all-around game.",
            "Can be exposed if forced into rushed decisions too often."
        ],
    },
]

MANAGERS = [
    "Carlo Mendes", "David Romero", "Nikos Papas", "Miguel Santos", "Luca Ferri",
    "Andreas Moretti", "Julian Costa", "Petros Marinakis", "Victor Salazar", "Marco Leone"
]

used_reviews = set()

def connect():
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASS,
        db=DB_NAME,
        charset="utf8mb4"
    )

def ensure_reviews_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS player_reviews (
            id INT NOT NULL AUTO_INCREMENT,
            student_id INT NOT NULL,
            manager_name VARCHAR(100) NOT NULL,
            archetype VARCHAR(100) NOT NULL,
            review_text TEXT NOT NULL,
            embedding VECTOR(384) NULL,
            PRIMARY KEY (id),
            KEY student_id (student_id),
            CONSTRAINT fk_player_reviews_student
              FOREIGN KEY (student_id) REFERENCES students (id)
              ON DELETE CASCADE ON UPDATE CASCADE
        )
    """)

def insert_review(cur, student_id, archetype):
    manager = random.choice(MANAGERS)
    review = build_review(archetype)
    cur.execute(
        "INSERT INTO player_reviews (student_id, manager_name, archetype, review_text, embedding) VALUES (%s, %s, %s, %s, NULL)",
        (student_id, manager, archetype["name"], review)
    )
def insert_student(cur, first_name, last_name, email):
    cur.execute(
        "INSERT INTO students (first_name, last_name, email) VALUES (%s, %s, %s)",
        (first_name, last_name, email)
    )
    return cur.lastrowid
def insert_grades(cur, student_id, archetype):
    for course, (lo, hi) in archetype["grade_ranges"].items():
        value = random.randint(lo, hi)
        cur.execute(
            "INSERT INTO grades (course_name, grade, student_id) VALUES (%s, %s, %s)",
            (course, value, student_id)
        )

def build_review(archetype):
    for _ in range(100):
        parts = [
            random.choice(archetype["openings"]),
            random.choice(archetype["strengths_1"]),
            random.choice(archetype["strengths_2"]),
            random.choice(archetype["tactical"]),
            random.choice(archetype["weaknesses"]),
        ]
        review = " ".join(parts)

        if review not in used_reviews:
            used_reviews.add(review)
            return review

    # fallback αν για κάποιο λόγο εξαντληθούν οι συνδυασμοί
    review = " ".join([
        random.choice(archetype["openings"]),
        random.choice(archetype["strengths_1"]),
        random.choice(archetype["strengths_2"]),
        random.choice(archetype["tactical"]),
        random.choice(archetype["weaknesses"]),
        f"Scout note #{random.randint(1000,9999)}."
    ])
    used_reviews.add(review)
    return review



def preload_existing_reviews(cur):
    cur.execute("SELECT review_text FROM player_reviews")
    rows = cur.fetchall()
    for row in rows:
        used_reviews.add(row[0])

def attach_reviews_to_existing_students(cur):
    cur.execute("SELECT id FROM students ORDER BY id")
    existing = cur.fetchall()
    for row in existing:
        student_id = row[0]
        cur.execute("SELECT COUNT(*) FROM player_reviews WHERE student_id = %s", (student_id,))
        count = cur.fetchone()[0]
        if count == 0:
            archetype = random.choice(ARCHETYPES)
            insert_review(cur, student_id, archetype)

def add_new_dummy_students(cur, count=200):
    for _ in range(count):
        archetype = random.choice(ARCHETYPES)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        student_id = insert_student(cur, first_name, last_name, email)
        insert_grades(cur, student_id, archetype)
        insert_review(cur, student_id, archetype)

def main():
    conn = connect()
    cur = conn.cursor()

    ensure_reviews_table(cur)
    preload_existing_reviews(cur)
    attach_reviews_to_existing_students(cur)
    add_new_dummy_students(cur, count=200)

    conn.commit()
    cur.close()
    conn.close()
    print("Done: reviews table ensured, existing students reviewed, 200 new dummy students added.")

if __name__ == "__main__":
    main()