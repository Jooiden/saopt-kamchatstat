program a1;
var a:array [1..100] of real;
    b:integer;
    c:byte;
begin
  readln(b);
  for c := 1 to b do
  begin
    readln(a[c]);
  end;
  write('Массив А [');
  for c := 1 to b do
  begin
    write(a[c],' ');
  end;
  write(']');
end.