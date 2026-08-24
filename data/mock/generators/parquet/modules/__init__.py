"""
Módulos geradores de dados mock por entidade do modelo de dados.
"""
from .clientes import ClientesGenerator, generate as generate_clientes
from .produtos import ProdutosGenerator, generate as generate_produtos
from .carrinhos import CarrinhosGenerator, generate as generate_carrinhos, save_df as save_carrinhos_df
from .itens_carrinho import ItensCarrinhoGenerator, generate as generate_itens_carrinho
from .eventos_carrinho import EventosCarrinhoGenerator, generate as generate_eventos_carrinho
from .eventos_resgate import EventosResgateGenerator, generate as generate_eventos_resgate
from .pedidos import PedidosGenerator, generate as generate_pedidos
