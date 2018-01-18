<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<!doctype html>
<html lang="en">

<head>

    <title>Login Page</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

</head>

<body>
                <!-- Login Form -->
                <form:form action="${pageContext.request.contextPath}/login_process" method="POST" class="form-horizontal">

                    <!-- Place for messages: error, alert etc ... -->
                    <div class="form-group">

                                <c:if test="${param.error != null}">

                                    <div class="alert alert-danger col-xs-offset-1 col-xs-10">
                                        Invalid username and password.
                                    </div>

                                </c:if>
                    </div>

                        <span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>

                        <input type="text" name="username" placeholder="username" class="form-control">

                        <span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>

                        <input type="password" name="password" placeholder="password" class="form-control" >

                    <button type="submit" class="btn btn-success">Login</button>

                </form:form>

</body>
</html>