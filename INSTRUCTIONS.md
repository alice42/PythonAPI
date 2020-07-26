### Using Postman

Authorization header is in the following format:

```
Key: Authorization
Value: "token_generated_during_login"
```

### Using api swagger

Provide the token generated during login in `Basic Auth(apiKey)` by clicking `Authorize`(general) or lock item(specific route)

### General Usage

Make sure you followed the [README](https://github.com/alice42/ApiArcane/blob/master/README.md) instructions.

## Create a user

Send a `POST` request to the `/user/` route with a `Content-Type: application/json`

```
{
	"email":"example@gmail.com",
	"username":"username",
	"password":"123456"
}

```

## Log in

Send a `POST` request to the `/auth/login` route with a `Content-Type: application/json`:

```
{
	"email":"example@gmail.com",
	"password":"123456"
}
```

## Log out

Send a `POST` request to the `/auth/logout` route.
(Authorization required)

## Edit user

Send a PATCH request with the fields to be modified to the `/user/<user_public_id>` with a `Content-Type: application/json`:
(Authorization required)

notice that `birthday` must be Iso8601 format

```
{
	"username":"newUsername"
}
```

## All users

Send a `GET` request to the `user/` route.
(Authorization required)

## Specific user

Send a `GET` request to the `user/<user_public_id>` route.
(Authorization required)

## Delete user

Only owner of the account can delete it
A deleted user will be logged out and the token blacklisted

Send a `DELETE` request to the `user/<user_public_id>` route.
(Authorization required)

## Create a property

Send a `POST` request to the `/property` route with a `Content-Type: application/json`
(Authorization required)

notice that `room_count` can't be 0

```
{
	"name":"a property name",
	"description":"a description",
	"property_type":"mansion",
	"city":"Paris",
	"rooms_count":2
}

```

## Edit a property

Only owner of the property can edit it

Send a `PATCH` request with the fields to be modified to the `/property/<property_public_id>` with a `Content-Type: application/json`:
(Authorization required)

notice that `room_count` can't be 0

```
{
	"name":"a new property name",
	"description":"a new description"
}
```

## All properties

Send a `GET` request to the `property/` route.
(Authorization required)

## Specific property

Send a `GET` request to the `property/<property_public_id>` route.
(Authorization required)

## Delete a property

Only owner of the property can edit it

Send a `DELETE` request to the `property/<property_public_id>` route.
(Authorization required)

## Find properties by city

Send a `GET` request to the `property/city/<city>` route.
(Authorization required)
