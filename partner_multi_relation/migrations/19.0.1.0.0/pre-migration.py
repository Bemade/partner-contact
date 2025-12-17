# Copyright 2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    logger.info("Delete obsolete SQL views")
    env.cr.execute("DROP VIEW IF EXISTS res_partner_relation_all;")
    env.cr.execute("DROP VIEW IF EXISTS res_partner_relation_type_selection;")
    logger.info("Renaming res_partner_relation_type columns")
    # In pre-migration, models are not loaded yet, so we use rename_columns
    # which works directly with table/column names without needing the ORM
    openupgrade.rename_columns(
        env.cr,
        {
            "res_partner_relation_type": [
                ("contact_type_left", "left_partner_type"),
                ("contact_type_right", "right_partner_type"),
                ("partner_category_left", "left_partner_category_id"),
                ("partner_category_right", "right_partner_category_id"),
            ],
        },
    )
