# stockBE

1. when users click on the website, a user can see the company’s info and about me.
   user will have to sign up/login

2. when user sign up, they will see:

<ul>
  <li>top nav bar</li>
  <li>logo takes you home</li>
  <li>search bar for stock</li>
  <li>favorite stock area</li>
  <li>setting button </li>
  <li>logout button</li>
</ul>

3. main page will show:
<ul>
  <li>top stock</li>
  <li>user can add stock to their favorite </li>
  <li>user can click on a stock</li>
  <li>once’s click it will show the name, price and info</li>
  <li>user can buy and sell stock that will be adjusted into their money</li>
</ul>

4. favorite stock section:

<ul>
  <li>user can see all their favorite stock</li>
  <li>user can add and delete stock </li>
  <li>options to click on stock and buy stock</li>
</ul>

5. setting area:

<ul>
  <li>user can add funds</li>
  <li>edit their username, email, password</li>
  <li>dalete, delete all user info. </li>
</ul>

6.logout button:

<ul>
<li>log user out</li>
</ul>

<h2>Routes:</h2>
  <tr>
    <th>Routes:</th>
    <th>Function:</th>
    <th>Methods:</th>
  </tr>
    <tr>
    <td>/user/login</td>
    <td>user login</td>
    <td>Post</td>
  </tr>
    <tr>
    <td>/user/signup</td>
    <td>user signup</td>
    <td>Post</td>
  </tr>
    <tr>
    <td>/user/verify</td>
    <td>verify user</td>
    <td>Get</td>
  </tr>
    <tr>
    <td>/user/edit</td>
    <td>user can edit</td>
    <td>Put</td>
  </tr>
    <tr>
    <td>/user/delete</td>
    <td>user delete</td>
    <td>Delete</td>
  </tr>
    <tr>
    <td>/stock</td>
    <td>get all stock</td>
    <td>get</td>
  </tr>
    <tr>
    <td>/stock/:id</td>
    <td>get one stock</td>
    <td>get</td>
  </tr>
    <tr>
    <td>/stock/add</td>
    <td>add stock</td>
    <td>post</td>
  </tr>
    <tr>
    <td>/stock/sell</td>
    <td>sell</td>
    <td>post</td>
  </tr>
