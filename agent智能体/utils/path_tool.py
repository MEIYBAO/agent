import os

def get_project_root()->str:
    '''获取根目录'''
    current_file = os.path.abspath(__file__)

    current_dir = os.path.dirname(current_file)

    project_root = os.path.dirname(current_dir)

    return project_root

def get_abs_path(relative_path) -> str:
    '''传递相对路径，得到绝对路径'''

    project_root = get_project_root()
    return os.path.join(project_root,relative_path)

if __name__ == '__main__':
    print(get_abs_path('config\config.txt'))
