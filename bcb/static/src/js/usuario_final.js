odoo.define('bcb.crear_empresa', function(require) {

    var publicWidget = require('web.public.widget');

    publicWidget.registry.websiteCrearEmpresa = publicWidget.Widget.extend({
        selector: '.crear_empresa_nueva',
        events : {
            'click #empresa_nueva': '_onClickCrearEmpresa',
        },
        _onClickCrearEmpresa: function(ev){
            var bcb_usuario_final = $(ev.currentTarget).attr('data-bcb-usuario-final');
            var empresa = $(ev.currentTarget).attr('data-valor-empresa');
            var rfc_empresa = $(ev.currentTarget).attr('data-valor-rfc');
            console.log(bcb_usuario_final);

            this._rpc({
                route: "/crear_empresa",
                params: {
                    'usuario_id': bcb_usuario_final,
                    'name': empresa,
                    'rfc': rfc_empresa,
                }
            }).then(function(data){
                console.log('data: '+data );
                //window.location = window.location.pathname //Refrescar el navegador
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