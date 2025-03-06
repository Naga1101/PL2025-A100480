# PL2025
## Aluno

**Nome:**  Nuno Aguiar

**Número:**  A100480

**Email:** a100480@alunos.uminho.pt

## Objetivo

Construir um analisador léxico para uma liguagem de query com a qual se podem escrever frases do
género:

```
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
``` 