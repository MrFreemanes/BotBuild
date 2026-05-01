from config.action_config import ActionType, ClickType
from config.widget_config import DirectionType

"""
NODE_REGISTRY - обозначение базовых значений, количество портов и их названия.
"""
inputs = DirectionType.INPUT
outputs = DirectionType.OUTPUT
NODE_REGISTRY = {
    ActionType.CLICK: {
        'base_params': {
            'node_id': None,
            'clicks': 1,
            'click_type': ClickType.LEFT.value
        },
        'ports': {
            inputs: ['input'],
            outputs: ['output']
        }
    },
    ActionType.WAIT: {
        'base_params': {
            'node_id': None,
            'waiting_time': 1
        },
        'ports': {
            inputs: ['input'],
            outputs: ['output']
        }
    },
    ActionType.IF: {
        'base_params': {
            'node_id': None,
        },
        'ports': {
            inputs: ['input'],
            outputs: ['action', 'actions_true', 'actions_false']
        }
    },
    ActionType.SEARCH_FOR_IF: {
        'base_params': {
            'node_id': None,
            'template_path': None
        },
        'ports': {
            inputs: ['if'],
            outputs: []
        }
    },
    ActionType.WAIT_UNTIL: {
        'base_params': {
            'node_id': None,
            'timeout': 0,
        },
        'ports': {
            inputs: ['input'],
            outputs: ['action', 'actions_true', 'actions_false']
        }
    },
    ActionType.SEARCH_FOR_WAIT_UNTIL: {
        'base_params': {
            'node_id': None,
            'template_path': None
        },
        'ports': {
            inputs: ['wait_until'],
            outputs: []
        }
    },
}
