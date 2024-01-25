use Vista_Replication_PRD
select distinct T.Origem, Es.Descricao, Cr.Gerente
from Tarefa T
inner join dw_vista.dbo.DM_Estrutura Es on Es.Id_estrutura = T.EstruturaId
inner join dw_vista.dbo.DM_CR cr on cr.Id_CR = Es.Id_CR
where cr.Gerente = 'denise dos santos dias silva' 
and T.Nome = 'Visita Oper. Liderança'
and MONTH(Disponibilizacao) = 01
and YEAR(Disponibilizacao) = 2024