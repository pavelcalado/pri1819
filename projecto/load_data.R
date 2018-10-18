library(manifestoR)
mp_setapikey("manifesto_apikey.txt")

numdocs <- mp_availability(TRUE)
numdocs
pt <- filter(numdocs, language == "portuguese")
pt_docs <- mp_corpus(pt)
ptdf <- as.data.frame(pt_docs, with.meta = TRUE)
write.csv(ptdf, "pt_docs.csv")

numdocs <- mp_availability(TRUE)
numdocs
en <- filter(numdocs, language == "english")
en_docs <- mp_corpus(en)
endf <- as.data.frame(en_docs, with.meta = TRUE)
write.csv(endf, "en_docs.csv")
