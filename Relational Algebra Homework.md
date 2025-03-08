## A)

sci_fi_genre $\leftarrow \Pi_{genre\_id}(\sigma_{genre\_name="Science"}(genre))$

sci_fi_books $\leftarrow (\Pi_{book\_id}(book\_genre \bowtie sci\_fi\_genre))\bowtie book$

sci_fi_authors $\leftarrow \Pi_{author\_id,name}(author \bowtie((writes\bowtie sci\_fi\_books)))$

## B)

downtown_branch $\leftarrow \Pi_{branch\_id}(\sigma_{location="Downtown"}(library\_branch))$

downtown_copies $\leftarrow \Pi_{copy\_id}(copy \bowtie downtown\_branch)$

downtown_borrowers $\leftarrow borrower \bowtie (\Pi_{borrower\_id}(loan \bowtie downtown\_copies))$
## C)

penguin_publisher $\leftarrow \Pi_{publisher\_id}(\sigma_{name="Penguin Books"}(publisher))$

penguin_books $\leftarrow \Pi_{book\_id}(book \bowtie penguin\_publisher)$

penguin_copies $\leftarrow \Pi_{copy\_id}(copy \bowtie penguin\_books)$

penguin_borrowers $\leftarrow \Pi_{borrower\_id,name}(borrower \bowtie (\Pi_{borrower\_id}(loan \bowtie penguin\_copies)))$

## D)

late_loans $\leftarrow \Pi_{borrower\_id}(\sigma_{return\_date>due\_date}(loan))$

late_borrowers $\leftarrow \Pi_{borrower\_id,name}(late\_loans \bowtie borrower)$

## E)

all_books $\leftarrow \Pi_{book\_id,title}(book)$

borrowed_books $\leftarrow \Pi_{book\_id,title}(\Pi_{book\_id}(\Pi_{copy\_id}(loan)\bowtie copy) \bowtie book)$

never_borrowed $\leftarrow all\_books-borrowed\_books$

## F)

