---
title: "Creating really simple API Authentication in .NET"
date: 2022-11-09T12:29:19Z
draft: false
type: "post"
---

# Creating 'really simple' API key authentication in .NET

Sometimes you're going to run into a situation where you need to add some level of authentication to your .NET API. 

If you're like me, the whole .NET authentication and authorization is pretty complicated. Especially when in a language like JavaScript, it's pretty simple to add middleware to a request and check to see whether a header is present in the request.

Here's a very simple version:
``` javascript
// using express
const authenticationMiddleware = function(req, res, next) => {
    const apiKeyHeader = req.Headers["x-api-key"] ?? "";
    const authenticatedKey = "1234567890"; // Environment variable or somewhere else secure

    if (!apiKeyHeader || apiKeyHeader != authenticatedKey) return res.status(401).send('You are not Authorised to access this endpoint.');

    next();
}
```

When it comes to .NET, we have a lot of built-in security. Something that JavaScript lacks without proper configuration.

I'm going to cover a very basic API Key based authentication example which is good enough to use.

## Getting set up

I've added the result of this tutorial to a git repository for you to pull down here: https://github.com/edleeman17/Api-Key-Authentication

We're going to be using the new `net7.0` version of .NET in this example. 

> But this solution should support projects down to `netcoreapp3.0`;

I've created a brand new project with OpenAPI support enabled. This means that we can run [Swagger](https://swagger.io/) to get a UI for our API endpoints.

For housekeeping reasons, I'm going to create a new directory named `Authentication`.

Create the following classes under that directory:
- `ApiKeyAuthenticationHandler.cs`
- `ApiKeyAuthenticationOptions.cs`
- `AuthenticationBuilderExtensions.cs`
- `UnauthorisedProblemDetails.cs`

## Building the Authentication Handler

Within our project, we'll need to create a new Authentication Handler. This is responsible for doing the actual API Key comparison.

> We're going to be extending the `AuthenticationHandler` from `MicrosoftAspNetCore.Authentication`.

First things first, we need to extend our class from the `AuthenticationHandler<ApiKeyAuthenticationOptions>` class.

``` java
public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
{}
```

Then we need to pad out the constructor to meet the base requirements.

``` java
public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
{
    public ApiKeyAuthenticationHandler(IOptionsMonitor<ApiKeyAuthenticationOptions> options, ILoggerFactory logger, UrlEncoder encoder, ISystemClock clock): base(options, logger, encoder, clock){}
}
```

We'll need to satisfy the error and add a new method override named `HandleChallengeAsync`.

``` java
public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
{
    public ApiKeyAuthenticationHandler(IOptionsMonitor<ApiKeyAuthenticationOptions> options, ILoggerFactory logger, UrlEncoder encoder, ISystemClock clock): base(options, logger, encoder, clock){}

    protected override async Task HandleChallengeAsync(AuthenticationProperties properties)
    {
        Response.StatusCode = 401;
        Response.ContentType = "application/problem+json";
        var problemDetails = new UnauthorisedProblemDetails();

        await Response.WriteAsync(JsonSerializer.Serialize(problemDetails));
    }
}
```

And a new method named `HandleAuthenticateAsync`.

``` java
public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
{
    public ApiKeyAuthenticationHandler(IOptionsMonitor<ApiKeyAuthenticationOptions> options, ILoggerFactory logger, UrlEncoder encoder, ISystemClock clock): base(options, logger, encoder, clock){}

    protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        return AuthenticateResult.Success(new AuthenticationTicket(new ClaimsPrincipal(), ApiKeyAuthenticationOptions.Scheme));
    }

    protected override async Task HandleChallengeAsync(AuthenticationProperties properties)
    {
        Response.StatusCode = 401;
        Response.ContentType = "application/problem+json";
        var problemDetails = new UnauthorisedProblemDetails();

        await Response.WriteAsync(JsonSerializer.Serialize(problemDetails));
    }
}
```

You might see some async/await errors, but we can ignore these for now. There may also be an error around `ApiKeyAuthenticationOptions` but we'll cover this in the next step.

## Creating ApiKeyAuthenticationOptions

As we're only creating a basic example, this class is pretty simple.

Add the following to `ApiKeyAuthenticationOptions.cs`.

``` java
public class ApiKeyAuthenticationOptions : AuthenticationSchemeOptions
{
    public const string DefaultScheme = "API Key";
    public static string Scheme => DefaultScheme;
}
```

This should remove the error we're seeing in `ApiKeyEuthenticationHandler.cs`.

## Creating UnauthorisedProblemDetails

We also need to add a new constructor to `UnauthorisedProblemDetails.cs`. This class extends from the new ProblemDetails class which specifies a machine-readable format for specifying errors in HTTP API responses.

``` java
public class UnauthorisedProblemDetails : ProblemDetails
{
    public UnauthorisedProblemDetails(string details = "")
    {
        Title = "Unauthorized";
        Detail = details;
        Status = 401;
        Type = "https://httpstatuses.com/401";
    }
}
```

## Creating AuthenticationBuilderExtensions

The next step in wiring this up is to create a new Extension method for ApplicationBuilder. This is so that when the project starts up, we register our new middleware methods to be called.

Add the following to `AuthenticationBuilderExtensions.cs`.

``` java
public static class AuthenticationBuilderExtensions
{
    public static AuthenticationBuilder AddApiKeySupport(this AuthenticationBuilder authenticationBuilder, Action<ApiKeyAuthenticationOptions> options)
    {
        return authenticationBuilder.AddScheme<ApiKeyAuthenticationOptions, ApiKeyAuthenticationHandler>(ApiKeyAuthenticationOptions.DefaultScheme, options);
    }
}
```

## Connecting the wires

Now that we have some base configuration setup, we can take a look at getting this working. We haven't defined any of the API Key comparisons yet, we'll be looking at that a bit further down.

What's important is that we have the correct configuration in `Program.cs` to get the middleware hooked up.

Firstly, navigate to `Program.cs` (or `Startup.cs` if you're not using `net7.0`).

From the `builder`, we need to add Authentication.

``` java
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services.AddAuthentication(); // <-- Add Authentication

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();
```

We then need to configure Authentication with our new `ApiKeyAuthenticationOptions` and our new `AddApiKeySupport` Extension method.

``` java
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services.AddAuthentication(options => 
{
    options.DefaultAuthenticateScheme = ApiKeyAuthenticationOptions.DefaultScheme;
    options.DefaultChallengeScheme = ApiKeyAuthenticationOptions.DefaultScheme;
}).AddApiKeySupport(_ => {}); // <-- Don't forget this!

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();
```

We then need to tell our API to use the built-in Authentication and Authorization. This allows us to use the `[Authorized]` method attributes for our methods.

``` java
using ApiKeyAuthentication.Authentication;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = ApiKeyAuthenticationOptions.DefaultScheme;
    options.DefaultChallengeScheme = ApiKeyAuthenticationOptions.DefaultScheme;
}).AddApiKeySupport(_ => { }); // <-- Don't forget this!

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseAuthentication(); // <-- Add this
app.UseAuthorization(); // <-- Add this

app.MapControllers();

app.Run();
```

## Adding Authorization attribute to our endpoints

Now that we have the wiring finally configured, we can add our Authorization attribute to the methods we want to lock down.

I'm just going to use the default WeatherForcast API endpoint that comes with the new project.

``` java
[Authorize] // <-- Added here
[HttpGet(Name = "GetWeatherForecast")]
public IEnumerable<WeatherForecast> Get()
{
    return Enumerable.Range(1, 5).Select(index => new WeatherForecast
    {
        Date = DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
        TemperatureC = Random.Shared.Next(-20, 55),
        Summary = Summaries[Random.Shared.Next(Summaries.Length)]
    })
    .ToArray();
}
```

I've added the attribute at a method level for more granular control. But you can also add the attribute at a class level so that all methods within the class require authorisation.

## Calling your endpoint

Now if you call your endpoint, you should see a 403 response. This means you're unauthorised. Nice one!

This might be confusing as if you remember in our `HandleAuthenticateAsync` we're returning a successful result. The reason this is happening is we're calling the method asynchronously, without actually awaiting anything. So we're not reaching the successful result in time for the authentication.

We can resolve this by temporarily adding an `await Task.Yield()` to our `HandleAuthenticateAsync` method.

``` java
protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
{
    await Task.Yield();
    return AuthenticateResult.Success(new AuthenticationTicket(new ClaimsPrincipal(), ApiKeyAuthenticationOptions.Scheme));
}
```

Once changed, you'll receive a 200 response again from the endpoint.

## Configuring an API Key

I'm going to build a very simple implementation of an API Key comparison. I'll be adding the key directly to the solution, it's recommended to use an environment variable or call an external key store like [Vault](https://www.vaultproject.io/)

Head back to `ApiKeyAuthenticationHandler.cs`. We're going to add some configuration.

We need to rewrite `HandleAuthenticateAsync`.

``` java
protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
{
    if (!Request.Headers.TryGetValue("X-API-KEY", out var apiKeyHeaderValue)) return AuthenticateResult.Fail("Authorisation Failure.");

    var allowedKeys = new [] { "my-valid-api-key-value" };

    if (!allowedKeys.Any(k => k.Equals(apiKeyHeaderValue)))
    {
        return AuthenticateResult.Fail("Authorisation Failure.");
    }

    var identity = new ClaimsIdentity( new[]{ new Claim(ClaimTypes.Name, Guid.NewGuid().ToString()) }, Scheme.Name);
    var principal = new System.Security.Principal.GenericPrincipal(identity, null);

    await Task.Yield();

    return AuthenticateResult.Success(new AuthenticationTicket(principal, ApiKeyAuthenticationOptions.Scheme));
}
```

The code above will look for a header in the request named `X-API-KEY`. It will then grab the value and compare it with our authorised API Key `my-valid-api-key-value`.

If the keys do not match, we'll return an Authorisation Failure, otherwise, we'll return a successful response to the Authentication handler.

We've kept the `await Task.Yield()` in as we're not calling off to an external key provider in this example.

## Finishing up

Now that we have everything configured, you should now be able to hit the endpoint with our new API Key. Resulting in either a 200 or 403 depending on whether you're specifying the correct API Key or not.

Hopefully, you've successfully got everything up and running. If not feel free to get in touch.

## Optional Swagger Configuration

What we have is a fully working configuration, but wouldn't it be cool if our Swagger UI reflected that our method required authentication?

Swagger has a cool option to specify the API within the UI, with indicators to which API endpoints require authentication.

Back in `Program.cs` we can add the following configuration.

``` java
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = $"{Assembly.GetExecutingAssembly().GetName().Name} API", Version = "v1" });
    options.AddSecurityDefinition("X-API-KEY", new OpenApiSecurityScheme()
    {
        In = ParameterLocation.Header,
        Name = "X-API-KEY", //header with api key
        Type = SecuritySchemeType.ApiKey,
    });
});
```

When spinning the API backup, you should see an `Authorize` option which opens a modal allowing you to set the API Key value.

This is cool, but it would be nicer if we could also see which specific endpoints require authentication, rather than all of the endpoints showing as authorised.

If you cast back to when I added the Authorize attribute at a method level rather than a class level. That was for this exact reason.

With Swagger, we can add what's called an `OperationFilter` which allows us to define some rules for which endpoint should show as an authorised endpoint in our Swagger UI.

Install the Nuget package named `Swashbuckle.AspNetCore.Filters`;

Then back in `Program.cs` we can add the following line to use our new filter.

``` java
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = $"{Assembly.GetExecutingAssembly().GetName().Name} API", Version = "v1" });
    options.AddSecurityDefinition("X-API-KEY", new OpenApiSecurityScheme()
    {
        In = ParameterLocation.Header,
        Name = "X-API-KEY", //header with api key
        Type = SecuritySchemeType.ApiKey,
    });

    options.OperationFilter<SecurityRequirementsOperationFilter>(); // <-- Add our filter here
});
```

If I was to create a new API endpoint without the Authorization attribute. In Swagger, it should only show the padlock icon for the endpoint that does require Authentication.

## Thanks for reading!

Thanks for taking the time to read through the post, hopefully, some of it is useful!

Please don't hesitate to reach out if you have any questions!
