def convert_windows_path(directory):
    """
    Convertir la ruta del directorio de Windows a Linux compatible con GVFS.
    
    Ejemplo: \\vs31.cuvenpetrol.cu\CUVENPETROL\Gerencia SHA\videos nuevos ->
             /run/user/1000/gvfs/smb-share:server=vs31.cuvenpetrol.cu,share=d$/CUVENPETROL/Gerencia SHA/videos nuevos
    
    Args:
        directory (str): Ruta del directorio en formato de Windows.
    
    Returns:
        str: Ruta del directorio convertida en formato compatible con GVFS.
    """
    # Puedes implementar tu propia lógica de conversión aquí según tus necesidades
    converted_path = directory.replace('\\\\', '/run/user/1000/gvfs/smb-share:server=')
    converted_path = converted_path.replace('\\', '/')
    converted_path = converted_path.replace('/', ',', 1)
    converted_path = converted_path.replace(' ', '%20')
    return converted_path
