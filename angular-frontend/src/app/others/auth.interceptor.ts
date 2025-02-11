import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const access_token = localStorage.getItem('access_token');

  let requestToSend = req;

  if(access_token) {
    const headers = req.headers.set("Authorization", `Bearer ${access_token}`);
    requestToSend = req.clone({
      headers: headers
    })
  }
  return next(requestToSend);
};
