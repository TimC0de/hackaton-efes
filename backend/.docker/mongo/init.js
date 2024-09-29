db.createUser({
    user: "dev",
    pwd: "dev",
    roles: [
        {
            role: "readWrite",
            db: "dev"
        }
    ]
});

db.createCollection("cvs");