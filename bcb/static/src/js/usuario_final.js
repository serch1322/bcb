odoo.define('website_product.agregar_producto', function(require) {

    var publicWidget = require('web.public.widget');

    //console.log('HOLA MUNDO!');

    publicWidget.registry.websiteAgregarProductoCarrito = publicWidget.Widget.extend({
        selector: '.agregar_producto_carrito',
        events : {
            'click #add_to_cart_custom': '_onClickAgregarPorducto',
        },
        _onClickAgregarPorducto: function(ev){
            var product_id = $(ev.currentTarget).attr('data-product-id');
            //console.log(product_id);

            this._rpc({
                route: "/website/productos/crearventa",
                params: {
                    'product_id': product_id
                }
            }).then(function(data){
                //console.log('data: '+data );
                window.location = window.location.pathname //Refrescar el navegador
            });
        },


    });

    /*
    publicWidget.registry.websiteMostrarImganen = publicWidget.Widget.extend({

    });
    */

    /*
    var Boton_Producto = $('#add_to_cart_custom');

    var _botonProducto = function (e) {
        console.log('HOLA MUNDO1!');
    };

    Boton_Producto.click(_botonProducto);
    */

});