var vm = new Vue({
    el: '#loginform',
    data: {
        host: 'http://127.0.0.1:8000',
        username: '',
        password: '',
        remember: false,

        error_username: false,
        error_pwd: false,

        error_msg: '',    // 提示信息
    },

    methods: {
        // 获取url路径参数
        get_query_string: function (name) {
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },

        // 检查用户名数据
        check_username: function(){
            if (!this.username) {
                this.error_username = true;
                this.error_msg = '请填写用户名';
            } else {
                this.error_username = false;
                this.error_msg = '';
            }
        },

        // 检查密码
        check_pwd: function(){
            if (!this.password) {
                this.error_msg = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
                this.error_msg = '';
            }
        },

        // 表单提交
        on_submit: function(){
            this.check_username();
            this.check_pwd();

            if (this.error_username === false
                && this.error_pwd === false) {

                var url = this.host+'/authorizations/';
                var params = {
                    username: this.username,
                    password: this.password
                };
                axios.post(url, params, {withCredentials: true})
                    .then(response => {
                        // 使用浏览器本地存储保存token
                        if (this.remember) {
                            // 记住登录
                            sessionStorage.clear();
                            localStorage.token = response.data.token;
                            localStorage.user_id = response.data.user_id;
                            localStorage.username = response.data.username;
                        } else {
                            // 未记住登录
                            localStorage.clear();
                            sessionStorage.token = response.data.token;
                            sessionStorage.user_id = response.data.user_id;
                            sessionStorage.username = response.data.username;
                        }

                        // 跳转页面
                        var return_url = get_query_string('next');
                        if (!return_url) {
                            return_url = '/goods.html';
                        }
                        location.href = return_url;

                    }) .catch(error => {
                            this.error_msg = '用户名或密码错误';

                    })
            }
        },
    }
});