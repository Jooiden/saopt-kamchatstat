program a1;
var a,b,c:array [1..100] of integer;
    d:byte;
    e,f:integer;
begin
  readln(e,f);
  for d := 1 to e do
  begin
    readln(a[d]);
  end;
  for d := 1 to f do
  begin
    readln(b[d]);
  end;
  for d := 1 to e do
  begin
    c[d] := a[d] + b[d];
  end;
  for d := 1 to e do
  begin    
    write(c[d],' ');
  end;
end.