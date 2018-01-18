<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<!doctype html>
<html lang="en">

<head>

    <title>Register</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
</head>

<body>

                Register
                <!-- Register Form -->
                <form:form action="${pageContext.request.contextPath}/register" method="POST" commandName="userRegisterForm">

                    <form:errors/>
                    <form:label path="username">Username</form:label>
                    <form:input path="username" required="required" />
                    <form:errors path="username"/>

                    <form:label path="firstName">FirstName</form:label>
                    <form:input path="firstName" required="required" />
                    <form:errors path="firstName"/>

                    <form:label path="lastName">LastName</form:label>
                    <form:input path="lastName" required="required" />
                    <form:errors path="lastName"/>

                    <form:label path="type">Type</form:label>
                    <form:input path="type" required="required" />
                    <form:errors path="type"/>

                    <form:label path="email">Email</form:label>
                    <form:input path="email" type="email" required="required"/>
                    <form:errors path="email"/>

                    <form:label path="password">Password</form:label>
                    <form:password path="password" required="required"/>
                    <form:errors path="password"/>

                    <form:label path="confirmPassword">Confirm Password</form:label>
                    <form:password path="confirmPassword" required="required"/>
                    <form:errors path="confirmPassword"/>

                    <button type="submit" class="btn btn-success">Register</button>

                </form:form>

</body>
</html>