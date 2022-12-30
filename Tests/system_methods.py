def add_path(paths: list[str], local_path: str) -> str:
    a = paths[0].split('\\')
    a[len(a) - 1] = local_path
    PATH = "\\".join(a)
    paths.append(PATH)
    return PATH