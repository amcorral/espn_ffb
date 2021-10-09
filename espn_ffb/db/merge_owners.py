from espn_ffb.db.database import db
from espn_ffb.db.model.matchups import Matchups
from espn_ffb.db.model.owners import Owners
from espn_ffb.db.model.records import Records
from espn_ffb.db.model.teams import Teams
import logging


def bulk_update_owner_id(table_class, owner_column, old_owner_id, new_owner_id):
    existing_records = db.session.query(table_class).filter(
        getattr(table_class, owner_column) == old_owner_id
    )
    count = existing_records.count()
    if count > 0:
        primary_key_names = [
            pk_column.name
            for pk_column in table_class.__table__.primary_key.columns.values()
        ]
        update_mappings = list()
        for r in existing_records:
            update = {pk: getattr(r, pk) for pk in primary_key_names}
            update[owner_column] = new_owner_id
            update_mappings.append(update)
        db.session.bulk_update_mappings(table_class, update_mappings)
        logging.info(
            "Updated {} for {} {}".format(owner_column, count, table_class.__name__)
        )


def merge_owners(old_owner_id, new_owner_id):
    old_owner_query = db.session.query(Owners).filter(Owners.id == old_owner_id)
    old_owner = old_owner_query.first()
    delete_old_owner = False if old_owner is None else True

    new_owner = (
        db.session.query(Owners).filter(Owners.id == new_owner_id).first()
    )
    if new_owner is None:
        raise ValueError("Owner with id {} not found".format(new_owner_id))

    logging.info(
        "Merging Owner with id {} into {} with id {}".format(
            old_owner_id, new_owner, new_owner_id
        )
    )

    # Update records
    bulk_update_owner_id(Records, "owner_id", old_owner_id, new_owner_id)
    # Update matchups
    bulk_update_owner_id(Matchups, "owner_id", old_owner_id, new_owner_id)
    bulk_update_owner_id(
        Matchups, "opponent_owner_id", old_owner_id, new_owner_id
    )
    # Update Teams
    bulk_update_owner_id(Teams, "owner_id", old_owner_id, new_owner_id)

    if delete_old_owner:
        logging.info("Deleting {} with id {}".format(old_owner, old_owner_id))
        old_owner_query.delete()

    db.session.commit()
