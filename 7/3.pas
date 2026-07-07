program a1;
var a:array [1..100] of integer;
    b:integer;
    c:byte;
begin
  readln(b);
  for c := 1 to b do
  begin
    readln(a[c]);
  end;
  for c := 1 to b do
  begin
    writeln(c,' элемент А = ',a[c]);
  end;
end.