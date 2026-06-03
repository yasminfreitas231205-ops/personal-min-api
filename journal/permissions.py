from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        return obj.author == request.user


class IsOwnerOrEditorReadOnly(permissions.BasePermission):
    """
    Permite que o owner edite/delete suas entradas.
    Permite que membros do grupo 'Editor' leiam qualquer entrada (somente leitura).
    """
    def has_object_permission(self, request, view, obj):
        # Métodos de leitura (GET, HEAD, OPTIONS) - permitir se é owner ou está no grupo Editor
        if request.method in permissions.SAFE_METHODS:
            # Owner sempre pode ler
            if obj.author == request.user:
                return True
            # Membros do grupo 'Editor' podem ler
            if request.user.groups.filter(name='Editor').exists():
                return True
            return False
        
        # Métodos de escrita (POST, PUT, PATCH, DELETE) - apenas owner pode fazer
        return obj.author == request.user