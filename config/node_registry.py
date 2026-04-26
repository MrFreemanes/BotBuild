from config.action_config import ActionType, ClickType

NODE_REGISTRY = {
    ActionType.CLICK: {
        'base_params': {
            'ClickType': ClickType.RIGHT.value
        },
        'ports': {
            'inputs': ['input'],
            'outputs': ['output']
        }
    },
    ActionType.WAIT: {
        'base_params': {
            'waiting_time': 1
        },
        'ports': {
            'inputs': ['input'],
            'outputs': ['output']
        }
    },
    ActionType.IF: {
        'base_params': {},
        'ports': {
            'inputs': ['input'],
            'outputs': ['action', 'true', 'false']
        }
    }
}
