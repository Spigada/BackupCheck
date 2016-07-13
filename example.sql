       01 PS-DRW-REC.

           03 PS-DRW-ALT-KEY-1.
               05 PS-DRW-STR-NO                PIC 9(3).
               05 PS-DRW-REG-NO                PIC 9(3).
               05 PS-DRW-KEY.
                   07 PS-DRW-NO                PIC 9(3).

           03 PS-DRW-DESC                      PIC X(30).
           03 PS-DRW-PRIME-USR-ID              PIC X(3).
           03 PS-DRW-PTD-SLS                   PIC S9(10)V9(2) COMP-3.
           03 PS-DRW-YTD-SLS                   PIC S9(10)V9(2) COMP-3.
           03 PS-DRW-PTD-OVRG                  PIC S9(8)V9(2) COMP-3.
           03 PS-DRW-PTD-SHRTG                 PIC S9(8)V9(2) COMP-3.
           03 PS-DRW-DEV-ID                    PIC X(15).
           03 PS-DRW-OPN-CODS                  PIC X(15).
           03 PS-DRW-UNPSTD-OVR-SHRT           PIC S9(8)V9(2) COMP-3.
           03 PS-DRW-NXT-PTD-SLS               PIC S9(10)V9(2) COMP-3.
           03 PS-DRW-NXT-PTD-OVRG              PIC S9(8)V9(2) COMP-3.
           03 PS-DRW-NXT-PTD-SHRTG             PIC S9(8)V9(2) COMP-3.
           03 PS-DRW-DEV-ID-2                  PIC X(15).
           03 ps_drw_opn_cods_2                PIC X(15).



ignore comments (done)
ignore PTD/YTD
ignore filler (done)
variable names lowercase, replace - with _ (done)
level 01 are table names (done)
level 88 should go into separate enumeration tables
put occurs into separate table
handle redefines

remove _rec suffix from table names (done)
remove prefix from field names (done)

pic contains V9    --> decimal       (done)
pic is 9(8)        --> datetime      (done)
pic is numeric     --> int           (done)
flg with pic x(1)  --> boolean       (done)
else               --> varchar(255)  (done)

add primary key   (done)
add foreign keys as bigint not null


create table xxxx(

    primary key(id)
)engine=innodb default charset=utf8;
		  
-- register table
create table ps_reg_rec(
    id                             bigint auto_increment not null,
    created_by                     varchar(3) not null default '',
    created_on                     datetime not null default '1990-01-01 00:00:00',
    updated_by                     varchar(3) not null default '',
    updated_on                     datetime not null default '1990-01-01 00:00:00',
    rowversion                     timestamp not null default current_timestamp on update current_timestamp,

	ps_reg_stuff                   varchar(255) not null default '',

	primary key(id),
	foreign key(xxx_id) references xxx(id)
)engine=innodb default charset=utf8;

-- drawer table (parent is register)
create table ps_drw_rec(
    id                             bigint auto_increment not null,
    created_by                     varchar(3) not null default '',
    created_on                     datetime not null default '1990-01-01 00:00:00',
    updated_by                     varchar(3) not null default '',
    updated_on                     datetime not null default '1990-01-01 00:00:00',
    rowversion                     timestamp not null default current_timestamp on update current_timestamp,

	str_id                         bigint not null,
	reg_id                         bigint not null,
	usr_id                         bigint not null,
	
    ps_drw_str_no                  varchar(255) not null default '',
    ps_drw_reg_no                  varchar(255) not null default '',
    ps_drw_no                      varchar(255) not null default '',
    ps_drw_desc                    varchar(255) not null default '',
    ps_drw_prime_usr_id            varchar(255) not null default '',
    ps_drw_ptd_sls                 varchar(255) not null default '',
    ps_drw_ytd_sls                 varchar(255) not null default '',
    ps_drw_ptd_ovrg                varchar(255) not null default '',
    ps_drw_ptd_shrtg               varchar(255) not null default '',
    
	ps_drw_unpstd_ovr_shrt         varchar(255) not null default '',
    ps_drw_nxt_ptd_sls             varchar(255) not null default '',
    ps_drw_nxt_ptd_ovrg            varchar(255) not null default '',
    ps_drw_nxt_ptd_shrtg           varchar(255) not null default '',
    
	primary key(id),
	foreign key(str_no) references ps_str_rec (id)
	foreign key(reg_no) references ps_reg_rec (id)
	foreign key(reg_no) references ps_reg_rec (id)
)engine=innodb default charset=utf8;


-- drawer-device bridge table
create table ps_drw_dev(
    id                             bigint auto_increment not null,
    created_by                     varchar(3) not null default '',
    created_on                     datetime not null default '1990-01-01 00:00:00',
    updated_by                     varchar(3) not null default '',
    updated_on                     datetime not null default '1990-01-01 00:00:00',
    rowversion                     timestamp not null default current_timestamp on update current_timestamp,

	drw_id                         bigint not null,
	foreign key(drw_id) references ps_drw_rec (id),
	reg_id                         bigint not null,

	primary key(id),
	foreign key(reg_id) references ps_reg_rec (id)
)engine=innodb default charset=utf8;

-- device table
create table ps_dev(
    id                             bigint auto_increment not null,
    created_by                     varchar(3) not null default '',
    created_on                     datetime not null default '1990-01-01 00:00:00',
    updated_by                     varchar(3) not null default '',
    updated_on                     datetime not null default '1990-01-01 00:00:00',
    rowversion                     timestamp not null default current_timestamp on update current_timestamp,

	ps_drw_dev_id                  varchar(255) not null default '',
    ps_drw_opn_cods                varchar(255) not null default '',
	
	primary key(id)
)engine=innodb default charset=utf8;