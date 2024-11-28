def grupo_usuario(request):
    if request.user.is_authenticated:
        is_manicurista = request.user.groups.filter(name='manicurista').exists()
        is_cliente = request.user.groups.filter(name='cliente').exists()
    else:
        is_manicurista = False
        is_cliente = False
    
    return {
        'is_manicurista': is_manicurista,
        'is_cliente': is_cliente
    }