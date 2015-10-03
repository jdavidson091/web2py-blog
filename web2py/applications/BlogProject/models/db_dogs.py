

db.define_table('dog', Field('name'), Field('owner_id', 'reference auth_user'))