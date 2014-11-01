;;

(import datetime
        [sqlalchemy [Column DateTime String Integer ForeignKey func
                     Enum Unicode Boolean SmallInteger Date
                     UniqueConstraint create-engine]]
        [sqlalchemy.orm [relationship backref sessionmaker]]
        [sqlalchemy.ext.declarative [declarative-base]]
        [sqlalchemy.types :as types])

(def *engine* (create-engine "sqlite:///bjgj.sqlite"))
(def Session (sessionmaker))
