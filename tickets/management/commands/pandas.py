from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
import os
from tickets.models import Ticket

class Command(BaseCommand):
    help = "find minimum, maximum & average price of tickets"

    def handle(self, *args, **options):
        queryset = Ticket.objects.all().values()
        # print('data :)', queryset, type(queryset))
        df = pd.DataFrame(queryset)
        # print("Data frame :)\n",df)
        
        # Converting Data Types
        # print("Price data type:Before ->", df["price"].dtype)
        df["price"] = df["price"].astype(float)
        # print("Price data type:After ->", df["price"].dtype)
        
        # statistics 
        count = df['price'].count()
        min_price = df['price'].min()   
        max_price = df['price'].max()   
        avg_price = df['price'].mean()
        std_price = df['price'].std() # Standard Deviation

        print("Total tickets:)", count)
        print("Minimum Price:)", min_price)
        print("Maximum Price:)", max_price)
        print("Average Price:)", avg_price)
        print("Standard Deviation:)", std_price)
        
        # print('Descriptive Statistics:) \n',df.describe()['price'])
        # print('Describe :)\n',df.describe())

        # # Using agg
        # print(df["price"].agg(["min", "max", "mean"]))

        # # shape
        # print('DF shape :)',df.shape)

        # # sorting price by asc / desc order
        # sorted_df = df.sort_values(by='price',ascending=True)
        # sorted_df2 = df.sort_values(by='user_id',ascending=True)
        # print('Sorted df by price :)\n', sorted_df)
        # print('Sorted df by user id :)\n', sorted_df2)

        # # filtering
        # filtered_df = df[df["price"] > 110]
        # filtered_df2 =  df[(df["price"] > 105) & (df["price"] < 110)]
        # print('Filtered df :)\n', filtered_df)
        # print('Filtered df2 :)\n',filtered_df2)

        # # Reordering Columns
        # df = df[['id', 'user_id','from_station_id', 'to_station_id', 'price', 'date']]
        # print('Reordered df :)\n',df)
        
        # Renaming Columns
        # df = df.rename(columns={'date': 'Created date'})
        # print('Renamed df :)', df)

        # # Changing index
        # df = df.set_index('id')
        # print('index df on user_id:)\n', df)

        # df = df.reset_index()
        # print('reset inde:)\n', df)

        # Unique Values
        # print('unique users :)',df['user_id'].unique())

        # value counts
        # print('value count :)', df['user_id'].value_counts())


        # # Scenario - Total amount spent by each unique user to buy tickets
        # amount_spent = df.groupby("user_id", as_index=False)["price"].agg(["count", "min", "max", "sum", "mean"]).rename(
        #     columns={
        #         "count":"count", 
        #         "min":"min_ticket_price", 
        #         "max":"max_ticket_price",
        #         "sum": "total_spent",
        #         "mean":"avg_ticket_price" 
        #     }
        # )
        # amount_spent2 = pd.pivot_table(df, values='price', index='user_id',aggfunc=['count','min','max','sum','mean'])
        # print('Table :)\n',amount_spent)
        # print('Table :)\n',amount_spent2)
        
        
        # # Most populer routes
        # route_usage = df.groupby(by=["from_station_id","to_station_id"]).size().sort_values(ascending=False)
        # print('Route usage :)\n', route_usage)

        # # Monthly spending
        # df["date"] = pd.to_datetime(df["date"])
        # monthly_spend = (df.groupby(df["date"].dt.to_period("M"))["price"].sum())
        # print('Monthly spend :)',monthly_spend)

        # # Saving to excel
        # df["date"] = pd.to_datetime(df["date"])
        # output_dir = os.path.join(settings.BASE_DIR,'tickets/management/commands/output')
        # os.makedirs(output_dir, exist_ok=True)

        # file_path = os.path.join(output_dir, "output.xlsx")
        # df.to_excel(file_path, index=False)
                
        




        
        
    

