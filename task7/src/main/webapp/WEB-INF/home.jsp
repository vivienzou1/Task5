<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="security" uri="http://www.springframework.org/security/tags" %>

<!doctype html>
<html lang="en">

<head>

	<title>Home</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<!-- Reference Bootstrap files -->
	<link rel="stylesheet"
		  href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>

	<script	src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

</head>

<style>
	table {
		font-family: arial, sans-serif;
		border-collapse: collapse;
		width: 100%;
	}

	td, th {
		border: 1px solid #dddddd;
		text-align: left;
		padding: 8px;
	}

	tr:nth-child(even) {
		background-color: #dddddd;
	}
</style>


<body>

<div>


	<form:form action="${pageContext.request.contextPath}/logout" method="post">
		<button type="submit" value="logout">logout</button>
	</form:form>

</div>

<div>

	<%--replace username with real username--%>
	<p>Welcome <security:authentication property="principal.username"/></p>

	<br><br>
	<security:authorize access="hasRole('CUSTOMER')">
		<%--account summary--%>
		<table>
			<thead>Account Summary</thead>
			<tbody>
			<tr>
				<td>Routing Number: </td>
				<td>${accountInfo.routingNum}</td>
			</tr>
			<tr>
				<th>Account Type</th>
				<th>Account Number</th>
				<th>Balance</th>
			</tr>
			<c:forEach items="${accountInfo.bankAccounts}" var="account">
				<tr>
					<td>${account.type}</td>
					<td>${account.accountNum}</td>
					<td>${account.balance}</td>
				</tr>
			</c:forEach>
			</tbody>
		</table>
	</security:authorize>

	<security:authorize access="hasRole('BANKER')">
		<h4>Open Account</h4>

		<form:form commandName="openAccountForm" method="post" action="/openAccount">

			<form:errors/>

			<div style="margin-bottom: 25px" class="input-group">
				<form:label path="firstName" >First Name: </form:label>
				<form:input path="firstName" required="required" />
				<form:errors path="firstName" />
			</div>

			<div style="margin-bottom: 25px" class="input-group">
				<form:label path="lastName" >Last Name: </form:label>
				<form:input path="lastName" required="required" />
				<form:errors path="lastName" />
			</div>

			<div style="margin-bottom: 25px" class="input-group">
				<form:label path="dob" >Date of Birth: </form:label>
				<form:input path="dob" required="required" type="date" />
				<form:errors path="dob" />
			</div>

			<div style="margin-bottom: 25px" class="input-group">
				<form:label path="username" >Username: </form:label>
				<form:input path="username" required="required" />
				<form:errors path="username" />
			</div>

			<!-- Open Account Button -->
			<div style="margin-top: 10px" class="form-group">
				<div class="col-sm-6 controls">
					<button type="submit" class="btn btn-success">Open Account</button>
				</div>
			</div>

		</form:form>

		<c:if test="${param.created != null}">
			<p>Account created successfully</p>
		</c:if>


		<br><br><br>

		<table>
			<thead>Here are all accounts including registered and non-registered</thead>

			<tbody>
				<tr>
					<th>First Name</th>
					<th>Last Name</th>
					<th>DOB</th>
					<th>Created Time</th>
					<th>Assigned</th>
					<th>Pin Number</th>
					<th>Username</th>
				</tr>
				<c:if test="${not empty accountInfoList}">
					<c:forEach items="${accountInfoList}" var="account">
						<tr>
							<td>${account.firstName}</td>
							<td>${account.lastName}</td>
							<td>${account.dob}</td>
							<td>${account.createdDate}</td>
							<td>${account.assigned}</td>
							<td>${account.pinNum}</td>
							<td>${account.username}</td>
						</tr>
					</c:forEach>
				</c:if>
			</tbody>
		</table>

		<p>${accountInfoListError}</p>

	</security:authorize>

</div>

</body>
</html>