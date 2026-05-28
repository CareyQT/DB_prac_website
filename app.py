from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

import os


app = Flask(__name__)
app.secret_key = 'tales_from_the_spiral_secret'


def get_db():
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASS', ''),
            database=os.environ.get('DB_NAME', 'tales_from_spiral')
        )
        return conn
    except Exception:
        return None


def query(sql, params=()):
    conn = get_db()
    if not conn:
        return None
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def execute(sql, params=()):
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    conn.close()
    return True



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/areas')
def areas():
    rows = query("SELECT * FROM Areas ORDER BY areaLevel") or []
    return render_template('areas.html', areas=rows)

@app.route("/reset", methods=["POST"])
def reset():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.callproc("ResetDatabase")   # calls your stored procedure
    conn.commit()
    
    cursor.close()
    conn.close()
    flash('Database reset successfully.', 'success')
    return render_template('index.html')

@app.route('/areas/add', methods=['GET', 'POST'])
def areas_add():
    if request.method == 'POST':
        areaID = request.form['areaID']
        areaLevel = request.form['areaLevel']
        if execute("INSERT INTO Areas (areaID, areaLevel) VALUES (%s, %s)", (areaID, areaLevel)):
            flash(f'Area "{areaID}" added successfully.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('areas'))
    return render_template('areas_form.html', action='Add', area=None)

@app.route('/areas/edit/<areaID>', methods=['GET', 'POST'])
def areas_edit(areaID):
    if request.method == 'POST':
        areaLevel = request.form['areaLevel']
        if execute("UPDATE Areas SET areaLevel=%s WHERE areaID=%s", (areaLevel, areaID)):
            flash(f'Area "{areaID}" updated.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('areas'))
    rows = query("SELECT * FROM Areas WHERE areaID=%s", (areaID,))
    if not rows:
        flash('Area not found.', 'error')
        return redirect(url_for('areas'))
    area = rows[0]
    return render_template('areas_form.html', action='Edit', area=area)

@app.route('/areas/delete/<areaID>', methods=['POST'])
def areas_delete(areaID):
    if execute("DELETE FROM Areas WHERE areaID=%s", (areaID,)):
        flash(f'Area "{areaID}" deleted.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('areas'))

# ─── HAZARDS ─────────────────────────────────────────────────────────────────

@app.route('/hazards')
def hazards():
    rows = query("SELECT * FROM Hazards ORDER BY damage") or []
    return render_template('hazards.html', hazards=rows)

@app.route('/hazards/add', methods=['GET', 'POST'])
def hazards_add():
    if request.method == 'POST':
        hid = request.form['hazardID']
        dmg = request.form['damage']
        if execute("INSERT INTO Hazards (hazardID, damage) VALUES (%s, %s)", (hid, dmg)):
            flash(f'Hazard "{hid}" added.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('hazards'))
    return render_template('hazards_form.html', action='Add', hazard=None)

@app.route('/hazards/edit/<hazardID>', methods=['GET', 'POST'])
def hazards_edit(hazardID):
    if request.method == 'POST':
        dmg = request.form['damage']
        if execute("UPDATE Hazards SET damage=%s WHERE hazardID=%s", (dmg, hazardID)):
            flash(f'Hazard "{hazardID}" updated.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('hazards'))
    rows = query("SELECT * FROM Hazards WHERE hazardID=%s", (hazardID,))
    if not rows:
        flash('Hazard not found.', 'error')
        return redirect(url_for('hazards'))
    hazard = rows[0]
    return render_template('hazards_form.html', action='Edit', hazard=hazard)

@app.route('/hazards/delete/<hazardID>', methods=['POST'])
def hazards_delete(hazardID):
    if execute("DELETE FROM Hazards WHERE hazardID=%s", (hazardID,)):
        flash(f'Hazard "{hazardID}" deleted.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('hazards'))

# ─── ENEMIES ─────────────────────────────────────────────────────────────────

@app.route('/enemies')
def enemies():
    rows = query("SELECT * FROM Enemies ORDER BY hp") or []
    return render_template('enemies.html', enemies=rows)

@app.route('/enemies/add', methods=['GET', 'POST'])
def enemies_add():
    if request.method == 'POST':
        eid = request.form['enemyID']
        hp = request.form['hp']
        dmg = request.form['damage']
        if execute("INSERT INTO Enemies (enemyID, hp, damage) VALUES (%s, %s, %s)", (eid, hp, dmg)):
            flash(f'Enemy "{eid}" added.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('enemies'))
    return render_template('enemies_form.html', action='Add', enemy=None)

@app.route('/enemies/edit/<enemyID>', methods=['GET', 'POST'])
def enemies_edit(enemyID):
    if request.method == 'POST':
        hp = request.form['hp']
        dmg = request.form['damage']
        if execute("UPDATE Enemies SET hp=%s, damage=%s WHERE enemyID=%s", (hp, dmg, enemyID)):
            flash(f'Enemy "{enemyID}" updated.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('enemies'))
    rows = query("SELECT * FROM Enemies WHERE enemyID=%s", (enemyID,))
    if not rows:
        flash('Enemy not found.', 'error')
        return redirect(url_for('enemies'))
    enemy = rows[0]
    return render_template('enemies_form.html', action='Edit', enemy=enemy)

@app.route('/enemies/delete/<enemyID>', methods=['POST'])
def enemies_delete(enemyID):
    if execute("DELETE FROM Enemies WHERE enemyID=%s", (enemyID,)):
        flash(f'Enemy "{enemyID}" deleted.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('enemies'))

# ─── ABILITIES ────────────────────────────────────────────────────────────────

@app.route('/abilities')
def abilities():
    rows = query("SELECT * FROM Abilities ORDER BY abilityID") or []
    return render_template('abilities.html', abilities=rows)

@app.route('/abilities/add', methods=['GET', 'POST'])
def abilities_add():
    if request.method == 'POST':
        aid = request.form['abilityID']
        dmg = request.form['damage'] or None
        if execute("INSERT INTO Abilities (abilityID, damage) VALUES (%s, %s)", (aid, dmg)):
            flash(f'Ability "{aid}" added.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('abilities'))
    return render_template('abilities_form.html', action='Add', ability=None)

@app.route('/abilities/edit/<abilityID>', methods=['GET', 'POST'])
def abilities_edit(abilityID):
    if request.method == 'POST':
        dmg = request.form['damage'] or None
        if execute("UPDATE Abilities SET damage=%s WHERE abilityID=%s", (dmg, abilityID)):
            flash(f'Ability "{abilityID}" updated.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('abilities'))
    rows = query("SELECT * FROM Abilities WHERE abilityID=%s", (abilityID,))
    if not rows:
        flash('Ability not found.', 'error')
        return redirect(url_for('abilities'))
    ability = rows[0]
    return render_template('abilities_form.html', action='Edit', ability=ability)

@app.route('/abilities/delete/<abilityID>', methods=['POST'])
def abilities_delete(abilityID):
    if execute("DELETE FROM Abilities WHERE abilityID=%s", (abilityID,)):
        flash(f'Ability "{abilityID}" deleted.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('abilities'))

# ─── NPCs ────────────────────────────────────────────────────────────────────

@app.route('/npcs')
def npcs():
    rows = query("SELECT * FROM NPCs ORDER BY npcID") or []
    return render_template('npcs.html', npcs=rows)

@app.route('/npcs/add', methods=['GET', 'POST'])
def npcs_add():
    areas = query("SELECT areaID FROM Areas") or []
    enemies = query("SELECT enemyID FROM Enemies") or []
    if request.method == 'POST':
        nid = request.form['npcID']
        hp = request.form['hp']
        quest = 1 if request.form.get('quest') else 0
        shopkeeper = 1 if request.form.get('shopkeeper') else 0
        areaID = request.form['areaID']
        enemyID = request.form['enemyID'] or None
        if execute("INSERT INTO NPCs (npcID, hp, quest, shopkeeper, areaID, enemyID) VALUES (%s,%s,%s,%s,%s,%s)",
                   (nid, hp, quest, shopkeeper, areaID, enemyID)):
            flash(f'NPC "{nid}" added.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('npcs'))
    return render_template('npcs_form.html', action='Add', npc=None, areas=areas, enemies=enemies)

@app.route('/npcs/edit/<npcID>', methods=['GET', 'POST'])
def npcs_edit(npcID):
    areas = query("SELECT areaID FROM Areas") or []
    enemies = query("SELECT enemyID FROM Enemies") or []
    if request.method == 'POST':
        hp = request.form['hp']
        quest = 1 if request.form.get('quest') else 0
        shopkeeper = 1 if request.form.get('shopkeeper') else 0
        areaID = request.form['areaID']
        enemyID = request.form['enemyID'] or None
        if execute("UPDATE NPCs SET hp=%s, quest=%s, shopkeeper=%s, areaID=%s, enemyID=%s WHERE npcID=%s",
                   (hp, quest, shopkeeper, areaID, enemyID, npcID)):
            flash(f'NPC "{npcID}" updated.', 'success')
        else:
            flash('Could not connect to database.', 'error')
        return redirect(url_for('npcs'))
    rows = query("SELECT * FROM NPCs WHERE npcID=%s", (npcID,))
    if not rows:
        flash('NPC not found.', 'error')
        return redirect(url_for('npcs'))
    npc = rows[0]
    return render_template('npcs_form.html', action='Edit', npc=npc, areas=areas, enemies=enemies)

@app.route('/npcs/delete/<npcID>', methods=['POST'])
def npcs_delete(npcID):
    if execute("DELETE FROM NPCs WHERE npcID=%s", (npcID,)):
        flash(f'NPC "{npcID}" deleted.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('npcs'))

# ─── INTERSECTION TABLES ──────────────────────────────────────────────────────

@app.route('/area_hazards')
def area_hazards():
    rows = query("SELECT * FROM Area_Hazards ORDER BY areaID") or []
    areas = query("SELECT areaID FROM Areas") or []
    hazards = query("SELECT hazardID FROM Hazards") or []
    return render_template('area_hazards.html', rows=rows, areas=areas, hazards=hazards)

@app.route('/area_hazards/add', methods=['POST'])
def area_hazards_add():
    areaID = request.form['areaID']
    hazardID = request.form['hazardID']
    if execute("INSERT INTO Area_Hazards (areaID, hazardID) VALUES (%s, %s)", (areaID, hazardID)):
        flash('Link added.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('area_hazards'))

@app.route('/area_hazards/delete', methods=['POST'])
def area_hazards_delete():
    areaID = request.form['areaID']
    hazardID = request.form['hazardID']
    if execute("DELETE FROM Area_Hazards WHERE areaID=%s AND hazardID=%s", (areaID, hazardID)):
        flash('Link removed.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('area_hazards'))

@app.route('/area_enemies')
def area_enemies():
    rows = query("SELECT * FROM Area_Enemies ORDER BY areaID") or []
    areas = query("SELECT areaID FROM Areas") or []
    enemies = query("SELECT enemyID FROM Enemies") or []
    return render_template('area_enemies.html', rows=rows, areas=areas, enemies=enemies)

@app.route('/area_enemies/add', methods=['POST'])
def area_enemies_add():
    areaID = request.form['areaID']
    enemyID = request.form['enemyID']
    if execute("INSERT INTO Area_Enemies (areaID, enemyID) VALUES (%s, %s)", (areaID, enemyID)):
        flash('Link added.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('area_enemies'))

@app.route('/area_enemies/delete', methods=['POST'])
def area_enemies_delete():
    areaID = request.form['areaID']
    enemyID = request.form['enemyID']
    if execute("DELETE FROM Area_Enemies WHERE areaID=%s AND enemyID=%s", (areaID, enemyID)):
        flash('Link removed.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('area_enemies'))

@app.route('/enemy_abilities')
def enemy_abilities():
    rows = query("SELECT * FROM Enemy_Abilities ORDER BY enemyID") or []
    enemies = query("SELECT enemyID FROM Enemies") or []
    abilities = query("SELECT abilityID FROM Abilities") or []
    return render_template('enemy_abilities.html', rows=rows, enemies=enemies, abilities=abilities)

@app.route('/enemy_abilities/add', methods=['POST'])
def enemy_abilities_add():
    enemyID = request.form['enemyID']
    abilityID = request.form['abilityID']
    if execute("INSERT INTO Enemy_Abilities (enemyID, abilityID) VALUES (%s, %s)", (enemyID, abilityID)):
        flash('Link added.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('enemy_abilities'))

@app.route('/enemy_abilities/delete', methods=['POST'])
def enemy_abilities_delete():
    enemyID = request.form['enemyID']
    abilityID = request.form['abilityID']
    if execute("DELETE FROM Enemy_Abilities WHERE enemyID=%s AND abilityID=%s", (enemyID, abilityID)):
        flash('Link removed.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('enemy_abilities'))

@app.route('/npc_abilities')
def npc_abilities():
    rows = query("SELECT * FROM NPC_Abilities ORDER BY npcID") or []
    npcs = query("SELECT npcID FROM NPCs") or []
    abilities = query("SELECT abilityID FROM Abilities") or []
    return render_template('npc_abilities.html', rows=rows, npcs=npcs, abilities=abilities)

@app.route('/npc_abilities/add', methods=['POST'])
def npc_abilities_add():
    npcID = request.form['npcID']
    abilityID = request.form['abilityID']
    if execute("INSERT INTO NPC_Abilities (npcID, abilityID) VALUES (%s, %s)", (npcID, abilityID)):
        flash('Link added.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('npc_abilities'))

@app.route('/npc_abilities/delete', methods=['POST'])
def npc_abilities_delete():
    npcID = request.form['npcID']
    abilityID = request.form['abilityID']
    if execute("DELETE FROM NPC_Abilities WHERE npcID=%s AND abilityID=%s", (npcID, abilityID)):
        flash('Link removed.', 'success')
    else:
        flash('Could not connect to database.', 'error')
    return redirect(url_for('npc_abilities'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7890, debug=True)
