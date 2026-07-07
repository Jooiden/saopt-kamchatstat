program a1;
function b1(a:integer):integer;
begin
  if((a = 0) or (a = 1)) then
  begin
    b1 := a;
  end
  else
  begin
    b1 := b1(a - 1) + b1(a - 2);
  end;
end;
var a:array[1..20] of integer;
    b:byte;
begin
  for b := 1 to 20 do
  begin
    a[b] := b1(b);
    write(a[b],' ');
  end;
end.