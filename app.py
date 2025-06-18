from routes import app, db, User

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # crea un primer usuario admin si no existe
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
