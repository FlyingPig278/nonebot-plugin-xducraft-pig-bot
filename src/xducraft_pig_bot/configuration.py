"""Independent per-group pig-query limits."""
from pydantic import Field, StrictBool, StrictInt
from xducraft_bot.shared.configuration import (
    ConfigModel, ConfigResource, ConfigSnapshot, PluginConfiguration,
    declare_config, validate_values,
)
from .data_manager import (
    DEFAULT_MAX_FORWARD_RESULTS, DEFAULT_QUERY_COOLDOWN_SECONDS,
    MAX_QUERY_COOLDOWN_SECONDS, pig_data_manager,
)


class PigGroup(ConfigModel):
    max_forward_results: StrictInt = Field(
        default=DEFAULT_MAX_FORWARD_RESULTS, ge=1, title="本群合并转发上限", description="查询匹配多张图片时最多随机发送的数量。",
        json_schema_extra={"x-ui-group": "查询", "x-ui-order": 1, "x-ui-scope": "group_only",
                           "x-ui-effect-phase": "runtime"},
    )
    query_cooldown_enabled: StrictBool = Field(
        False, title="查询冷却", description="开启后，本群所有成员共用一个倒计时。",
        json_schema_extra={"x-ui-group": "查询", "x-ui-order": 2, "x-ui-scope": "group_only",
                           "x-ui-effect-phase": "runtime"},
    )
    query_cooldown_seconds: StrictInt = Field(
        DEFAULT_QUERY_COOLDOWN_SECONDS, ge=1, le=MAX_QUERY_COOLDOWN_SECONDS,
        title="冷却时长（秒）",
        json_schema_extra={"x-ui-group": "查询", "x-ui-order": 3, "x-ui-scope": "group_only",
                           "x-ui-effect-phase": "runtime"},
    )

def bind_configuration(manager):
    def read_group(ctx):
        values = manager.export_group_config(ctx.group_id)
        return ConfigSnapshot(values, revision_data=values)

    def write_group(ctx, values):
        manager.update_group_config(ctx.group_id, validate_values(PigGroup, values))

    return PluginConfiguration(
        key="pig_bot", name="猪猪图", resources={
            "group": ConfigResource(PigGroup, read_group, write_group),
        }, feature_keys=("pig_query", "pig_auto_push"),
        list_groups=manager.list_configured_groups,
        migrate_legacy=manager.migrate_legacy_config,
    )


DECLARATION = declare_config(bind_configuration(pig_data_manager))
