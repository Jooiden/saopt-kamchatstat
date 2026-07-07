program a1;
var a:array [1..5,1..5] of integer;
    b,c:byte;
    d,e,f:integer;
begin
  d := 0;
  e := 0;
  f := 0;
  for b := 1 to 5 do
  begin
    for c := 1 to 5 do
    begin
      a[b,c] := random(15) + 20;
    end;
  end;
  for b := 1 to 5 do
  begin
    for c := 1 to 5 do
    begin
      write(a[b,c],' ');
    end;
    writeln('');
  end;
  for b := 1 to 5 do
  begin
    if(b = 1) then
    begin
      for c := 1 to 5 do
      begin
        d := d + a[b,c];
      end;
    end;
    if(b = 5) then
    begin
      for c := 1 to 5 do
      begin
        e := e + a[b,c];
      end;
    end;  
    if(b = 3) then
    begin
      f := a[b,1];
      for c := 1 to 5 do
      begin
        if(a[b,c] > f) then
        begin
          f := a[b,c];
        end;
      end;
    end;
  end;
  if(d < e) then
  begin
    writeln('На 5 курсе обучается больше студентов, чем на 1. ');
  end
  else
  begin
    if(d = e) then
    begin
      writeln('На 1 и на 5 курсе обучается одинаковое количество студентов. ');      
    end
    else
    begin
      writeln('На 1 курсе обучается больше студентов, чем на 5. ');      
    end;
  end;
  writeln('Самая большая группа на 3 курсе ',f,'.');
end.