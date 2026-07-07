program a1;
var a:array[1..10] of integer;
    b:byte;
begin
  for b := 1 to 10 do
  begin
    a[b] := random(10);
  end;
  for b := 1 to 10 do
  begin
    write(a[b], ' ');
  end;
end.