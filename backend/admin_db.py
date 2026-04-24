"""
Admin Database Utility Script
Run from the backend folder: python admin_db.py

Commands:
  python admin_db.py users          - List all users
  python admin_db.py resumes        - List all resumes
  python admin_db.py scores         - List all ATS scores
  python admin_db.py skills <uid>   - List skills for a user
  python admin_db.py roadmap <uid>  - List roadmap for a user
  python admin_db.py promote <email> - Make a user admin
  python admin_db.py demote <email>  - Remove admin access
  python admin_db.py stats          - Show overall statistics
  python admin_db.py export         - Export all data to CSV files
"""
import sys
import csv
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal
from models import User, Resume, ATSScore, UserSkill, Roadmap


def get_db():
    return SessionLocal()


def list_users():
    db = get_db()
    users = db.query(User).all()
    print(f"\n{'='*70}")
    print(f"  {'ID':<5} {'Name':<20} {'Email':<35} {'Admin':<6} {'Created'}")
    print(f"{'='*70}")
    for u in users:
        print(f"  {u.user_id:<5} {u.name:<20} {u.email:<35} {'YES' if u.is_admin else 'No':<6} {str(u.created_at)[:19]}")
    print(f"\n  Total: {len(users)} users\n")
    db.close()


def list_resumes():
    db = get_db()
    resumes = db.query(Resume).all()
    print(f"\n{'='*90}")
    print(f"  {'ID':<5} {'User':<5} {'Filename':<30} {'Format':<7} {'Domain':<25} {'Date'}")
    print(f"{'='*90}")
    for r in resumes:
        print(f"  {r.resume_id:<5} {r.user_id:<5} {r.filename[:28]:<30} {r.file_format:<7} {str(r.selected_domain or '-')[:23]:<25} {str(r.uploaded_at)[:19]}")
    print(f"\n  Total: {len(resumes)} resumes\n")
    db.close()


def list_scores():
    db = get_db()
    scores = db.query(ATSScore).all()
    print(f"\n{'='*70}")
    print(f"  {'ID':<5} {'User':<5} {'Resume':<8} {'Score':<8} {'Date'}")
    print(f"{'='*70}")
    for s in scores:
        bar = "█" * int(s.total_score / 5) + "░" * (20 - int(s.total_score / 5))
        print(f"  {s.score_id:<5} {s.user_id:<5} {s.resume_id:<8} {s.total_score:<8} {bar} {str(s.scored_at)[:19]}")
    print(f"\n  Total: {len(scores)} scores\n")
    db.close()


def list_user_skills(user_id):
    db = get_db()
    skills = db.query(UserSkill).filter(UserSkill.user_id == int(user_id)).all()
    print(f"\n  Skills for User {user_id}: {len(skills)} found")
    print(f"{'='*60}")
    for s in skills:
        print(f"  {s.skill_name:<30} Score: {s.match_score:.2f}  Source: {s.source}")
    db.close()


def list_user_roadmap(user_id):
    db = get_db()
    items = db.query(Roadmap).filter(Roadmap.user_id == int(user_id)).order_by(Roadmap.week_number).all()
    total = len(items)
    completed = sum(1 for i in items if i.is_completed)
    print(f"\n  Roadmap for User {user_id}: {total} items, {completed} completed ({round(completed/max(total,1)*100)}%)")
    print(f"{'='*70}")
    current_week = None
    for i in items:
        if i.week_number != current_week:
            current_week = i.week_number
            print(f"\n  Week {current_week}:")
        status = "✅" if i.is_completed else "⬜"
        print(f"    {status} {i.skill_name:<25} ({i.estimated_hours}h)")
    db.close()


def promote_user(email):
    db = get_db()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"  User with email '{email}' not found")
    else:
        user.is_admin = True
        db.commit()
        print(f"  ✅ {user.name} ({user.email}) is now ADMIN")
    db.close()


def demote_user(email):
    db = get_db()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"  User with email '{email}' not found")
    else:
        user.is_admin = False
        db.commit()
        print(f"  ❌ {user.name} ({user.email}) admin access removed")
    db.close()


def show_stats():
    db = get_db()
    users = db.query(User).count()
    resumes = db.query(Resume).count()
    scores = db.query(ATSScore).all()
    skills = db.query(UserSkill).count()
    roadmaps = db.query(Roadmap).count()
    completed = db.query(Roadmap).filter(Roadmap.is_completed == True).count()

    avg_score = sum(s.total_score for s in scores) / max(len(scores), 1)

    print(f"\n  {'='*40}")
    print(f"  📊 DATABASE STATISTICS")
    print(f"  {'='*40}")
    print(f"  👥 Users:           {users}")
    print(f"  📄 Resumes:         {resumes}")
    print(f"  📊 ATS Scores:      {len(scores)}")
    print(f"  📈 Average Score:   {avg_score:.1f} / 100")
    print(f"  🎯 Skills Tracked:  {skills}")
    print(f"  🗺️  Roadmap Items:   {roadmaps}")
    print(f"  ✅ Completed:       {completed}")
    print(f"  {'='*40}\n")
    db.close()


def export_csv():
    db = get_db()
    export_dir = os.path.join(os.path.dirname(__file__), "exports")
    os.makedirs(export_dir, exist_ok=True)

    # Users
    with open(os.path.join(export_dir, "users.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["user_id", "name", "email", "is_admin", "created_at"])
        for u in db.query(User).all():
            w.writerow([u.user_id, u.name, u.email, u.is_admin, u.created_at])

    # Resumes
    with open(os.path.join(export_dir, "resumes.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["resume_id", "user_id", "filename", "file_format", "selected_domain", "uploaded_at"])
        for r in db.query(Resume).all():
            w.writerow([r.resume_id, r.user_id, r.filename, r.file_format, r.selected_domain, r.uploaded_at])

    # Scores
    with open(os.path.join(export_dir, "ats_scores.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["score_id", "user_id", "resume_id", "total_score", "scored_at"])
        for s in db.query(ATSScore).all():
            w.writerow([s.score_id, s.user_id, s.resume_id, s.total_score, s.scored_at])

    print(f"\n  ✅ Exported to: {export_dir}/")
    print(f"     - users.csv")
    print(f"     - resumes.csv")
    print(f"     - ats_scores.csv\n")
    db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "users":
        list_users()
    elif cmd == "resumes":
        list_resumes()
    elif cmd == "scores":
        list_scores()
    elif cmd == "skills" and len(sys.argv) > 2:
        list_user_skills(sys.argv[2])
    elif cmd == "roadmap" and len(sys.argv) > 2:
        list_user_roadmap(sys.argv[2])
    elif cmd == "promote" and len(sys.argv) > 2:
        promote_user(sys.argv[2])
    elif cmd == "demote" and len(sys.argv) > 2:
        demote_user(sys.argv[2])
    elif cmd == "stats":
        show_stats()
    elif cmd == "export":
        export_csv()
    else:
        print(__doc__)
