#encoding "utf8"

Place -> Word<kwtype=place>;
Person -> Word<kwtype=person>;

//find_fact -> (Word*) (Comma*) (Hyphen*) (Word*) Place (Word*) (Hyphen*) (Punct*) (Comma*) (Word*);
//find_fact -> (Word*) (Comma*) (Hyphen*) (Word*) Person (Word*) (Hyphen*) (Punct*) (Comma*) (Word*);

find_fact -> (AnyWord*) (Word<kwtype=person>*) Place (Word<kwtype=person>*) (AnyWord*);
find_fact -> (AnyWord*) (Word<kwtype=place>*) Person (Word<kwtype=place>*) (AnyWord*);


