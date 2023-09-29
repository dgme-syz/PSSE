#CSRF
开启并默认添加在request.headers
```javascript
var csrfToken = "{{ csrf_token }}";
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
```
