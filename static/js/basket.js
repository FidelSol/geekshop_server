$(document).ready(function () {

     $(document).on('click', 'input[type="number"]', function(event) {
            var target = event.target;
            $.ajax({
                url: '/baskets/edit/?id=' + target.name + '&quantity=' + target.value,
                success: function (data) {
                    if('result' in data){
                        $('.basket_list').html(data.result);
                    }
                },
            });
     })

     $(document).on('click', '[id^=add_]', function(event) {
            var target = event.target;
            target = target.id.split('_')[1]
            console.log(target)

            $.ajax({
                url: '/baskets/add/?product_id=' + target,
                success: function (data) {
                   console.log('yes')
                },
            });
     })


});
