from .basic_players import John1,AllIn
try:
    from .poker_players_training import training_opponents, John3
    __all__ = ['John1', 'John3', 'AllIn', 'training_opponents']
except ImportError:
    import sys
    supported_platforms = ['win32', 'linux', 'darwin']
    supported_versions = [11,12,13]
    print('WARNING: Failed to import the training opponents!')
    print('Supported platforms are:', ' '.join(supported_platforms))
    print('Supported versions are:', ' '.join([f'3.{v}' for v in supported_versions]))
    print(f'You are running Python {sys.version_info.major}.{sys.version_info.minor} on {sys.platform}.')
    if sys.platform not in supported_platforms:
        print('Please use a supported platform.')
    elif sys.version_info.major != 3 or sys.version_info.minor not in supported_versions:
        print('Please upgrade to a supported version of Python.')
    else:
        print('You appear to be running a supported version and platform. Linux .so files may be missing.')
    print('Continuing with basic players only (John1, AllIn)...\n')
    training_opponents = []
    John3 = None
    __all__ = ['John1', 'AllIn']
